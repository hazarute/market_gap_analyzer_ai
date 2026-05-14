import sys
from typing import Any

import requests


_ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
_ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


def _itunes_request(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def search_apps(keyword: str, n_hits: int = 10) -> list[dict[str, Any]]:
    """Anahtar kelimeyle Apple App Store'da arama yapar."""
    try:
        results = _itunes_request(
            _ITUNES_SEARCH_URL,
            {
                "term": keyword,
                "country": "tr",
                "entity": "software",
                "limit": n_hits,
            },
        ).get("results", [])
    except Exception as exc:
        print(f"[!] App Store arama hatası ('{keyword}'): {exc}", file=sys.stderr)
        return []

    apps: list[dict[str, Any]] = []
    for item in results:
        app_id = str(item.get("trackId") or item.get("collectionId") or "")
        if not app_id:
            continue

        apps.append(
            {
                "app_id": app_id,
                "app_name": item.get("trackName") or keyword,
                "store": "ios",
                "score": float(item.get("averageUserRating") or 0.0),
                "description": item.get("description", "") or item.get("formattedPrice", ""),
                "developer": item.get("sellerName") or item.get("artistName") or "",
                "rating_count": int(item.get("userRatingCount") or 0),
            }
        )

    if not apps:
        print(f"[!] App Store'da '{keyword}' için uygulama bulunamadı.", file=sys.stderr)
    return apps


def get_app_details(app_id: str) -> dict[str, Any]:
    """Verilen app_id için App Store'dan detaylı bilgi çeker."""
    try:
        data = _itunes_request(
            _ITUNES_LOOKUP_URL,
            {"id": app_id, "country": "tr", "entity": "software"},
        )
        result = data.get("results", [])
        if not result:
            raise ValueError("Lookup sonucu boş")

        item = result[0]
        description = item.get("description", "")
        return {
            "app_id": app_id,
            "app_name": item.get("trackName") or app_id,
            "store": "ios",
            "score": float(item.get("averageUserRating") or 0.0),
            "description": description,
            "reviews": [],
            "developer": item.get("sellerName") or item.get("artistName") or "",
            "rating_count": int(item.get("userRatingCount") or 0),
        }
    except Exception as exc:
        print(f"[!] App Store detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr)
        return {
            "app_id": app_id,
            "app_name": app_id,
            "store": "ios",
            "score": 0.0,
            "description": "",
            "reviews": [],
            "developer": "",
            "rating_count": 0,
        }
