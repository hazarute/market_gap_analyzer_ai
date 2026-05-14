---
applyTo: "scrapers/**/*.py"
---

# Scraper Kuralları — Market Gap Analyzer AI

## Sorumluluk Sınırı

Scraper katmanı **yalnızca veri toplar**. Analiz, prompt yönetimi, rapor üretimi veya veritabanı işlemi bu katmanda yapılmaz.

## Kütüphaneler

- `google-play-scraper` — Google Play Store
- `app-store-scraper` — Apple App Store

## Standart Çıktı Yapısı

Her scraper fonksiyonu aşağıdaki anahtar setine sahip sözlük listesi döndürür:

```python
{
    "app_id": str,          # paket adı veya store ID
    "app_name": str,        # uygulamanın adı
    "store": str,           # "android" veya "ios"
    "score": float,         # kullanıcı puanı (0.0–5.0)
    "description": str,     # uygulama açıklaması
    "reviews": list[str],   # kullanıcı yorumları (isteğe bağlı)
    "rating_count": int,    # yorum sayısı (isteğe bağlı)
    "developer": str,       # geliştirici adı (isteğe bağlı)
}
```

Zorunlu alanlar: `app_id`, `app_name`, `store`, `score`, `description`.

## Zorunlu Fonksiyonlar

```python
# scrapers/google_play.py
def search_apps(keyword: str, n_hits: int = 10) -> list[dict]:
    """Anahtar kelimeyle Google Play'de arama yapar."""

def get_app_details(app_id: str) -> dict:
    """Verilen app_id için detaylı bilgi ve yorumları çeker."""

# scrapers/app_store.py
def search_apps(keyword: str, n_hits: int = 10) -> list[dict]:
    """Anahtar kelimeyle App Store'da arama yapar."""

def get_app_details(app_id: str) -> dict:
    """Verilen app_id için detaylı bilgi ve yorumları çeker."""
```

## Hata Yönetimi

- Ağ hatası, boş sonuç ve zaman aşımı `try/except` ile yakalanır.
- Hata durumunda kullanıcıya açıklayıcı mesaj verilir; uygulama çökmez.
- Boş arama sonucu durumunda boş liste döndürülür ve kullanıcıya bilgi verilir.
- Rate limit durumunda hata mesajı loglama yapılır ve pipeline sonraki adıma geçer.

## Modül Yapısı

```
scrapers/
├── __init__.py         # boş veya ortak import
├── google_play.py      # Google Play scraper
└── app_store.py        # App Store scraper
```

## Genişletme Kuralı

Yeni mağaza desteği eklenecekse `scrapers/` altına yeni modül eklenir. Standart çıktı yapısı korunmalıdır; `main.py` ve `analyzer.py` değişmeden çalışmaya devam etmelidir.
