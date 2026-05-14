import argparse
import sys

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
        choices=STORE_CHOICES,
        help="Hedef mağaza: 'android' (Google Play) veya 'ios' (App Store)",
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
    return parser.parse_args()


def run(
    keyword: str,
    store: str,
    limit: int,
    opportunity_map: bool = False,
    master_prompt: bool = False,
) -> None:
    # --master-prompt veya --all-stages, --opportunity-map'i de gerektirir.
    run_opportunity_map = opportunity_map or master_prompt
    run_master_prompt = master_prompt

    conn = database.init_db(config.DATABASE_PATH)

    try:
        print(f"\n[*] '{keyword}' için {store} mağazası taranıyor...")

        if store == "android":
            apps = gp_search(keyword, n_hits=limit)
            get_details = gp_details
        else:
            apps = as_search(keyword, n_hits=limit)
            get_details = as_details

        if not apps:
            print("[!] Arama sonucu bulunamadı.")
            return

        print(f"[+] {len(apps)} uygulama bulundu.\n")

        for app in apps:
            app_id: str = app["app_id"]
            app_name: str = app["app_name"]

            if database.is_analyzed(conn, app_id):
                print(f"[~] '{app_name}' daha önce analiz edilmiş, atlanıyor.")
                continue

            print(f"[>] '{app_name}' analiz ediliyor...")

            try:
                detailed = get_details(app_id)
                analysis_result = analyze_app(detailed)
                report_path = generate_report(app_name, analysis_result, detailed)
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
                    opp_path = map_opportunity(report_path, app_name)
                    database.save_opportunity_map(conn, app_id, opp_path)
                    print(f"[✓] Fırsat haritası kaydedildi: {opp_path}")

                if run_master_prompt:
                    print(f"[>] '{app_name}' için master prompt sentezleniyor...")
                    mp_path = create_master_prompt(report_path, opp_path, app_name)
                    database.save_master_prompt(conn, app_id, mp_path)
                    print(f"[✓] Master prompt kaydedildi: {mp_path}")

            except Exception as exc:
                print(f"[!] '{app_name}' işlemi başarısız: {exc}", file=sys.stderr)
                continue

    finally:
        conn.close()


def main() -> None:
    args = parse_args()
    run(
        keyword=args.keyword,
        store=args.store,
        limit=args.limit,
        opportunity_map=args.opportunity_map or args.all_stages,
        master_prompt=args.master_prompt or args.all_stages,
    )


if __name__ == "__main__":
    main()
