import sys
from typing import Any

from google_play_scraper import app as gp_app
from google_play_scraper import search as gp_search
from google_play_scraper import reviews as gp_reviews
from google_play_scraper import Sort

# Google Play Store JSON şema değişikliği nedeniyle oluşan top search result "appId": None sorununu çözmek için runtime yaması:
from google_play_scraper.constants.element import ElementSpecs
if hasattr(ElementSpecs, "SearchResultOnTop") and "appId" in ElementSpecs.SearchResultOnTop:
    ElementSpecs.SearchResultOnTop["appId"].data_map = [3, "12", 0, 0]



def search_apps(
    keyword: str,
    n_hits: int = 10,
    offset: int = 0,
    lang: str = "tr",
    country: str = "tr",
) -> list[dict[str, Any]]:
    """Anahtar kelimeyle Google Play Store'da arama yapar.

    Args:
        keyword: Arama terimi
        n_hits: Döndürülecek sonuç sayısı
        offset: Atlanacak sonuç sayısı (sayfalama için)
        lang: Dil kodu
        country: Ülke kodu

    Returns:
        Standart uygulama sözlüğü listesi.
        Her eleman: app_id, app_name, store, score, description içerir.
    """
    try:
        # Google Play API'sinin offset desteği olmadığı için daha büyük sonuç alıp sonradan dilimleme yap
        results = gp_search(keyword, n_hits=n_hits + offset, lang=lang, country=country)
    except Exception as exc:
        print(f"[!] Google Play arama hatası ('{keyword}'): {exc}", file=sys.stderr)
        return []

    # Offset'e göre dilimleme
    results = results[offset : offset + n_hits]

    apps: list[dict[str, Any]] = []
    for item in results:
        apps.append(
            {
                "app_id": item.get("appId", ""),
                "app_name": item.get("title", ""),
                "store": "android",
                "score": float(item.get("score") or 0.0),
                "description": item.get("description") or item.get("summary", ""),
                "developer": item.get("developer", ""),
                "rating_count": item.get("ratings", 0),
            }
        )
    return apps


def _fetch_filtered_reviews(
    app_id: str,
    count_target: int,
    sort: Sort,
    filter_score_with: int = None,
    lang: str = "tr",
    country: str = "tr",
) -> list[dict]:
    """İstenen sayıda en az 10 kelimelik yorum çeker."""
    try:
        # 10 kelimelik yorumları filtreleyebilmek için başlangıçta 100 yorum çekiyoruz.
        results, _ = gp_reviews(
            app_id,
            lang=lang,
            country=country,
            sort=sort,
            count=100,
            filter_score_with=filter_score_with,
        )
        if not results:
            return []

        filtered = []
        for r in results:
            content = r.get("content")
            if content:
                words = content.split()
                if len(words) >= 10:
                    filtered.append(r)
                    if len(filtered) >= count_target:
                        break
        return filtered
    except Exception as exc:
        print(
            f"[!] Yorum filtreleme ve çekme hatası (score={filter_score_with}): {exc}",
            file=sys.stderr,
        )
        return []


def get_app_details(app_id: str, lang: str = "tr", country: str = "tr") -> dict[str, Any]:
    """Verilen app_id için Google Play'den detaylı bilgi ve yorumları çeker.

    Returns:
        Standart uygulama sözlüğü; reviews listesi de içerir.
    """
    try:
        detail = gp_app(app_id, lang=lang, country=country)
    except Exception as exc:
        print(
            f"[!] Google Play detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr
        )
        detail = {}

    # Eğer Türkçe arandıysa ve puan/değerlendirme bulunamadıysa (veya hata alındıysa) en/us fallback'i dene
    if lang == "tr" and country == "tr" and (not detail or detail.get("ratings", 0) == 0):
        print(f"[*] '{app_id}' için Türkçe puan/değerlendirme bulunamadı, 'en' ve 'us' fallback sorgulanıyor...", file=sys.stderr)
        try:
            fallback_detail = gp_app(app_id, lang="en", country="us")
            if fallback_detail and fallback_detail.get("ratings", 0) > 0:
                detail = fallback_detail
                lang, country = "en", "us"
        except Exception as exc:
            print(f"[!] Google Play fallback detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr)

    if not detail:
        return {
            "app_id": app_id,
            "app_name": app_id,
            "store": "android",
            "score": 0.0,
            "description": "",
            "reviews": [],
            "developer": "",
            "rating_count": 0,
        }

    # 1. En Alakalı Yorumlar - en fazla 20 adet (en az 10 kelimelik)
    rel_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, lang=lang, country=country)
    # 2. Negatif Yorumlar (1 Yıldız) - en fazla 20 adet (en az 10 kelimelik)
    neg_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, filter_score_with=1, lang=lang, country=country)
    # 3. Pozitif Yorumlar (5 Yıldız) - en fazla 20 adet (en az 10 kelimelik)
    pos_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, filter_score_with=5, lang=lang, country=country)

    # Eğer yorum bulunamadıysa ve tr/tr dilindeysek bir de en/us yorum fallback dene
    if lang == "tr" and country == "tr" and not rel_result and not neg_result and not pos_result:
        print(f"[*] '{app_id}' için Türkçe yorum bulunamadı, 'en' ve 'us' yorum fallback sorgulanıyor...", file=sys.stderr)
        rel_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, lang="en", country="us")
        neg_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, filter_score_with=1, lang="en", country="us")
        pos_result = _fetch_filtered_reviews(app_id, count_target=20, sort=Sort.MOST_RELEVANT, filter_score_with=5, lang="en", country="us")

    review_texts: list[str] = []
    seen_contents = set()
    for r in (rel_result or []) + (neg_result or []) + (pos_result or []):
        content = r.get("content")
        if content and content not in seen_contents:
            seen_contents.add(content)
            review_texts.append(content)

    return {
        "app_id": app_id,
        "app_name": detail.get("title", app_id),
        "store": "android",
        "score": float(detail.get("score") or 0.0),
        "description": detail.get("description", ""),
        "reviews": review_texts,
        "developer": detail.get("developer", ""),
        "rating_count": detail.get("ratings", 0),
    }
