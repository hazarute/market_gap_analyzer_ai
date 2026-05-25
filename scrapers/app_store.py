import sys
from typing import Any

import requests


_ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
_ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


def _itunes_request(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def search_apps(
    keyword: str,
    n_hits: int = 10,
    offset: int = 0,
    country: str = "tr",
) -> list[dict[str, Any]]:
    """Anahtar kelimeyle Apple App Store'da arama yapar.

    Args:
        keyword: Arama terimi
        n_hits: Döndürülecek sonuç sayısı
        offset: Atlanacak sonuç sayısı (sayfalama için)
        country: Ülke kodu (varsayılan: "tr")

    Note:
        iTunes Search API `offset` parametresini güvenilir şekilde desteklemez.
        Google Play ile aynı strateji uygulanır: n_hits + offset kadar sonuç alınır,
        sonra offset'e göre dilimleme yapılır.
    """
    try:
        results = _itunes_request(
            _ITUNES_SEARCH_URL,
            {
                "term": keyword,
                "country": country,
                "entity": "software",
                "limit": n_hits + offset,
            },
        ).get("results", [])
    except Exception as exc:
        print(f"[!] App Store arama hatası ('{keyword}'): {exc}", file=sys.stderr)
        return []

    results = results[offset : offset + n_hits]

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


def _fetch_app_store_reviews(
    app_id: str,
    country: str = "tr",
    count_target: int = 20,
    filter_score_with: int = None,
) -> list[str]:
    """iTunes RSS beslemesinden en az 10 kelimelik yorumları çeker."""
    try:
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        data = response.json()
        feed = data.get("feed", {})
        entries = feed.get("entry", [])
        if not entries:
            return []
        
        if isinstance(entries, dict):
            entries = [entries]
            
        filtered_reviews: list[str] = []
        for entry in entries:
            content = entry.get("content", {}).get("label")
            if not content:
                continue
            
            # Kelime sayısı kontrolü
            words = content.split()
            if len(words) < 10:
                continue
                
            # Skor filtresi (varsa)
            if filter_score_with is not None:
                rating = entry.get("im:rating", {}).get("label")
                if rating != str(filter_score_with):
                    continue
            
            filtered_reviews.append(content)
            if len(filtered_reviews) >= count_target:
                break
                
        return filtered_reviews
    except Exception as exc:
        print(f"[!] App Store yorum çekme hatası (country={country}): {exc}", file=sys.stderr)
        return []


def get_app_details(app_id: str, country: str = "tr") -> dict[str, Any]:
    """Verilen app_id için App Store'dan detaylı bilgi çeker."""
    try:
        data = _itunes_request(
            _ITUNES_LOOKUP_URL,
            {"id": app_id, "country": country, "entity": "software"},
        )
        result = data.get("results", [])
    except Exception as exc:
        print(f"[!] App Store detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr)
        result = []

    # Eğer Türkçe arandıysa ve puan/değerlendirme bulunamadıysa (veya lookup boş döndüyse) en/us fallback'i dene
    if country == "tr" and (not result or result[0].get("userRatingCount", 0) == 0):
        print(f"[*] '{app_id}' için Türkçe App Store puan/değerlendirme bulunamadı, 'us' fallback sorgulanıyor...", file=sys.stderr)
        try:
            fallback_data = _itunes_request(
                _ITUNES_LOOKUP_URL,
                {"id": app_id, "country": "us", "entity": "software"},
            )
            fallback_result = fallback_data.get("results", [])
            if fallback_result and fallback_result[0].get("userRatingCount", 0) > 0:
                result = fallback_result
                country = "us"
        except Exception as exc:
            print(f"[!] App Store fallback detay çekme hatası ('{app_id}'): {exc}", file=sys.stderr)

    if not result:
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

    item = result[0]
    description = item.get("description", "")

    # Yorumları çek
    # 1. En Alakalı/Son Yorumlar - en fazla 20 adet (en az 10 kelimelik)
    rel_result = _fetch_app_store_reviews(app_id, country=country, count_target=20)
    # 2. Negatif Yorumlar (1 Yıldız) - en fazla 20 adet (en az 10 kelimelik)
    neg_result = _fetch_app_store_reviews(app_id, country=country, count_target=20, filter_score_with=1)
    # 3. Pozitif Yorumlar (5 Yıldız) - en fazla 20 adet (en az 10 kelimelik)
    pos_result = _fetch_app_store_reviews(app_id, country=country, count_target=20, filter_score_with=5)

    # Eğer yorum bulunamadıysa ve country="tr" dilindeysek bir de "us" yorum fallback dene
    if country == "tr" and not rel_result and not neg_result and not pos_result:
        print(f"[*] '{app_id}' için Türkçe App Store yorumu bulunamadı, 'us' yorum fallback sorgulanıyor...", file=sys.stderr)
        rel_result = _fetch_app_store_reviews(app_id, country="us", count_target=20)
        neg_result = _fetch_app_store_reviews(app_id, country="us", count_target=20, filter_score_with=1)
        pos_result = _fetch_app_store_reviews(app_id, country="us", count_target=20, filter_score_with=5)

    review_texts: list[str] = []
    seen_contents = set()
    for content in (rel_result or []) + (neg_result or []) + (pos_result or []):
        if content and content not in seen_contents:
            seen_contents.add(content)
            review_texts.append(content)

    return {
        "app_id": app_id,
        "app_name": item.get("trackName") or app_id,
        "store": "ios",
        "score": float(item.get("averageUserRating") or 0.0),
        "description": description,
        "reviews": review_texts,
        "developer": item.get("sellerName") or item.get("artistName") or "",
        "rating_count": int(item.get("userRatingCount") or 0),
    }
