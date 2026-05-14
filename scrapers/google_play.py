import sys
from typing import Any

from google_play_scraper import app as gp_app
from google_play_scraper import search as gp_search
from google_play_scraper import reviews as gp_reviews
from google_play_scraper import Sort


def search_apps(keyword: str, n_hits: int = 10) -> list[dict[str, Any]]:
    """Anahtar kelimeyle Google Play Store'da arama yapar.

    Returns:
        Standart uygulama sözlüğü listesi.
        Her eleman: app_id, app_name, store, score, description içerir.
    """
    try:
        results = gp_search(keyword, n_hits=n_hits, lang="tr", country="tr")
    except Exception as exc:
        print(f"[!] Google Play arama hatası ('{keyword}'): {exc}", file=sys.stderr)
        return []

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


def get_app_details(app_id: str) -> dict[str, Any]:
    """Verilen app_id için Google Play'den detaylı bilgi ve yorumları çeker.

    Returns:
        Standart uygulama sözlüğü; reviews listesi de içerir.
    """
    try:
        detail = gp_app(app_id, lang="tr", country="tr")
    except Exception as exc:
        print(
            f"[!] Google Play detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr
        )
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

    review_texts: list[str] = []
    try:
        result, _ = gp_reviews(
            app_id,
            lang="tr",
            country="tr",
            sort=Sort.MOST_RELEVANT,
            count=20,
        )
        review_texts = [r["content"] for r in (result or []) if r.get("content")]
    except Exception as exc:
        print(f"[!] Google Play yorum çekme hatası ('{app_id}'): {exc}", file=sys.stderr)

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
