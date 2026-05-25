import argparse
import re
import sys
from pathlib import Path

import config
import database
from analyzer import analyze_app
from opportunity_mapper import map_opportunity
from prompt_synthesizer import create_master_prompt
from report_generator import generate_report
from scrapers.google_play import get_app_details as gp_details
from scrapers.google_play import search_apps as gp_search
from scrapers.app_store import get_app_details as as_details
from scrapers.app_store import search_apps as as_search

STORE_CHOICES = ("android", "ios")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Market Gap Analyzer AI — App store analiz otomasyonu"
    )
    parser.add_argument(
        "--keyword",
        required=True,
        help="Arama anahtar kelimesi (örn: 'Proje Yönetimi')",
    )
    parser.add_argument(
        "--store",
        required=True,
        nargs="+",
        choices=STORE_CHOICES,
        help="Hedef mağaza(lar): 'android' (Google Play) ve/veya 'ios' (App Store)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Analiz edilecek maksimum uygulama sayısı (varsayılan: 10)",
    )
    parser.add_argument(
        "--opportunity-map",
        action="store_true",
        default=False,
        help="Aşama 2: Her rapor için LangChain ile fırsat haritası üret",
    )
    parser.add_argument(
        "--master-prompt",
        action="store_true",
        default=False,
        help="Aşama 3: Frontier LLM için master prompt sentezle (--opportunity-map'i de etkinleştirir)",
    )
    parser.add_argument(
        "--all-stages",
        action="store_true",
        default=False,
        help="Tüm aşamaları çalıştır: analiz + fırsat haritası + master prompt",
    )
    parser.add_argument(
        "--stars",
        type=float,
        default=None,
        help="Yalnızca belirtilen puan (ve üzeri) değerlendirmeye sahip uygulamaları analiz et",
    )
    return parser.parse_args()


def _normalize_app_name(app_name: str) -> str:
    normalized = app_name.lower()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def run(
    keyword: str,
    stores: list[str],
    limit: int,
    opportunity_map: bool = False,
    master_prompt: bool = False,
    stars: float = None,
) -> None:
    # --master-prompt veya --all-stages, --opportunity-map'i de gerektirir.
    run_opportunity_map = opportunity_map or master_prompt
    run_master_prompt = master_prompt
    normalized_stores = list(dict.fromkeys(stores))

    conn = database.init_db(config.DATABASE_PATH)
    # DB'deki mevcut app adlarını normalize ederek seen_names'e yükle.
    # Bu sayede önceki run'larda farklı store'dan analiz edilmiş aynı uygulama
    # bu run'da tekrar işlenmez (cross-run, cross-store duplikasyon önleme).
    seen_names: set[str] = {
        _normalize_app_name(name)
        for name in database.get_analyzed_app_names(conn)
    }

    try:
        for store in normalized_stores:
            print(f"\n[*] '{keyword}' için {store} mağazası taranıyor...")

            get_details = gp_details if store == "android" else as_details
            
            analyzed_count = 0
            offset = 0
            max_total_fetch = limit * 20  # güvenlik sınırı: en fazla 20 batch
            
            # Bu store'da analiz edilmek üzere seçilmiş adların çalıştırma esnasındaki duplikasyonunu önlemek için:
            seen_in_run = set()

            while analyzed_count < limit and offset < max_total_fetch:
                search_fn = gp_search if store == "android" else as_search
                batch = search_fn(keyword, n_hits=limit, offset=offset)
                if not batch:
                    break
                
                for app in batch:
                    app_id = app["app_id"]
                    app_name = app["app_name"]
                    normalized_name = _normalize_app_name(app_name)
                    
                    if database.is_analyzed(conn, app_id):
                        continue
                        
                    if normalized_name in seen_names or normalized_name in seen_in_run:
                        continue
                        
                    print(f"[>] '{app_name}' analiz ediliyor...")
                    try:
                        detailed = get_details(app_id)
                        
                        # Yıldız filtresi (stars) kontrolü - Yetersiz yıldız durumunda veritabanına eklenmeden atlanır
                        score = detailed.get("score") or 0.0
                        if stars is not None and score < stars:
                            print(f"[~] '{app_name}' yıldız filtresine takıldı (Puanı: {score} < {stars}). Veritabanına kaydedilmeden atlanıyor...")
                            continue
                        
                        # Yetersiz puan veya yorum durumunda analizi atla ve veritabanına "skipped" olarak kaydet
                        rating_count = detailed.get("rating_count") or 0
                        reviews = detailed.get("reviews") or []
                        if rating_count == 0 or len(reviews) == 0:
                            print(f"[-] '{app_name}' için yeterli puanlama veya yorum bulunamadı (Puanlama: {rating_count}, Yorum: {len(reviews)}). Analiz atlanıyor...")
                            database.save_analysis(
                                conn,
                                app_id,
                                app_name,
                                store,
                                "skipped",
                                detailed.get("description"),
                            )
                            seen_in_run.add(normalized_name)
                            continue

                        # Başarılı analiz
                        analysis_result = analyze_app(detailed)
                        report_path = generate_report(app_name, analysis_result, detailed, store=store)
                        database.save_analysis(
                            conn,
                            app_id,
                            app_name,
                            store,
                            report_path,
                            detailed.get("description"),
                        )
                        print(f"[✓] Rapor kaydedildi: {report_path}")

                        if run_opportunity_map:
                            print(f"[>] '{app_name}' için fırsat haritası üretiliyor...")
                            reports_dir = str(Path("reports") / store)
                            opp_path = map_opportunity(report_path, app_name, reports_dir=reports_dir)
                            database.save_opportunity_map(conn, app_id, opp_path)
                            print(f"[✓] Fırsat haritası kaydedildi: {opp_path}")

                        if run_master_prompt:
                            print(f"[>] '{app_name}' için master prompt sentezleniyor...")
                            mp_path = create_master_prompt(
                                report_path,
                                opp_path,
                                app_name,
                                reports_dir=reports_dir,
                            )
                            database.save_master_prompt(conn, app_id, mp_path)
                            print(f"[✓] Master prompt kaydedildi: {mp_path}")
                        
                        analyzed_count += 1
                        seen_in_run.add(normalized_name)
                        
                        if analyzed_count >= limit:
                            break
                            
                    except Exception as exc:
                        print(f"[!] '{app_name}' işlemi başarısız: {exc}", file=sys.stderr)
                        continue
                
                offset += limit
            
            # Bir sonraki store için cross-store duplikasyon önleme listesini güncelle
            seen_names.update(seen_in_run)
            
            # Mağaza analizi bittiğinde özet bilgi verelim
            if analyzed_count == 0:
                if stars is not None:
                    print(f"[!] '{keyword}' için {store} mağazasında {stars} yıldız ve üzeri puana sahip analiz edilebilecek yeni uygulama bulunamadı.")
                else:
                    print(f"[!] '{keyword}' için {store} mağazasında analiz edilebilecek yeni uygulama bulunamadı.")
            else:
                print(f"[+] {store} mağazasında {analyzed_count} yeni uygulama başarıyla analiz edildi.")

    finally:
        conn.close()


def main() -> None:
    args = parse_args()
    run(
        keyword=args.keyword,
        stores=args.store,
        limit=args.limit,
        opportunity_map=args.opportunity_map or args.all_stages,
        master_prompt=args.master_prompt or args.all_stages,
        stars=args.stars,
    )


if __name__ == "__main__":
    main()
