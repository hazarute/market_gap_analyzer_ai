# Coding Standards

## Isimlendirme Kurallari

- **Fonksiyonlar ve değişkenler:** `snake_case` (Python standardı)
- **Sınıflar:** `PascalCase` (gerekirse; bu projede sınıf kullanımı minimal)
- **Sabitler:** `UPPER_SNAKE_CASE` (örn: `DATABASE_PATH`, `OPENROUTER_MODEL`)
- **Modül/dosya adları:** `snake_case.py` (örn: `google_play.py`, `report_generator.py`)
- **Rapor dosyaları:** `rapor_<uygulama_adi>.md` formatı; uygulama adındaki boşluklar alt çizgiye dönüştürülür
- **Veritabanı tablo adı:** `analiz_gecmisi` (sabit, değiştirilemez)
- **Veritabanı dosyası:** `analiz_gecmisi.db` (varsayılan; `.env` ile override edilebilir)

## Dosya ve Klasor Kurallari

- Her modül tek bir sorumluluğa sahiptir (SRP)
- `scrapers/` klasörü yalnızca scraper modülleri içerir; `__init__.py` dahil
- Gizli yapılandırma yalnızca `.env` dosyasında yaşar; `config.py` bu değerleri okur
- `.env` dosyası asla commit edilmez; `.env.example` şablon olarak commit edilir
- Üretilen raporlar (`rapor_*.md`) ve veritabanı (`analiz_gecmisi.db`) `.gitignore`'a eklenir

## Mimari Kurallar

- **Katman bağımlılıkları:** `main.py` → `scrapers/`, `database.py`, `analyzer.py`, `report_generator.py`
  - Alt katmanlar birbirini doğrudan import etmez; orkestrasyonu `main.py` yapar
- **Scraper çıktı yapısı:** Her scraper fonksiyonu standart sözlük döndürür:
  ```python
  {
      "app_id": str,
      "app_name": str,
      "store": str,         # "android" veya "ios"
      "score": float,
      "description": str,
      "reviews": list[str], # isteğe bağlı; detay çekiminde doldurulur
  }
  ```
- **Veritabanı fonksiyonları:** `init_db()`, `is_analyzed(app_id: str) -> bool`, `save_analysis(...)`
- **Analyzer fonksiyonu:** `analyze_app(app_data: dict) -> str` — AI analiz metnini döndürür
- **Report generator fonksiyonu:** `generate_report(app_name: str, analysis_result: str) -> str` — dosya yolunu döndürür

## Hata Yonetimi

- Scraper katmanında ağ hataları ve boş sonuçlar için `try/except` blokları kullanılır; hata mesajı kullanıcıya iletilir
- LLM çağrısı başarısız olursa (`analyzer.py`) istisna yakalanır, loglama yapılır ve pipeline sonraki uygulamaya geçer
- Veritabanı bağlantı hatalarında açıklayıcı mesaj üretilir; uygulama çökmez
- `config.py` zorunlu `.env` değerlerini doğrular; eksik değer varsa `ValueError` fırlatır ve mesajda hangi değişkenin eksik olduğu belirtilir
- Doğrulama yalnızca sistem sınırlarında (giriş noktaları) yapılır; iç fonksiyonlarda gereksiz savunmacı kontrol eklenmez

## Test Yaklasimi

- Uçtan uca test: gerçek API anahtarıyla `main.py` çalıştırılarak pipeline doğrulanır
- Birim test: `database.py` fonksiyonları için geçici SQLite dosyasıyla izole test yazılabilir
- Scraper testleri: gerçek ağ isteği yerine mock veya kayıtlı yanıt kullanılır (API bağımlılığını kırmak için)
- Test çerçevesi: `pytest` (henüz bağımlılıklar arasına eklenmedi; Faz 4'te eklenecek)
- Test dosyaları: `tests/` klasöründe `test_<modül>.py` formatında

## Teknolojiye Ozel Notlar

**Python:**
- Minimum Python 3.10; `match` ifadesi ve `|` union tipi söz dizimi kullanılabilir
- Type hint'ler yeni yazılan fonksiyonlarda kullanılır; mevcut koda zorla eklenmez
- `python-dotenv` ile `.env` yükleme: `from dotenv import load_dotenv; load_dotenv()` modül düzeyinde çağrılır

**SQLite:**
- `sqlite3` standart kütüphanesi kullanılır; üçüncü taraf ORM eklenmez
- Parametreli sorgular zorunludur (`?` yer tutucu); SQL injection riski sıfırlanır
- `analiz_gecmisi` tablosu `init_db()` ile `CREATE TABLE IF NOT EXISTS` ile oluşturulur

**OpenRouter / OpenAI İstemcisi:**
- `base_url="https://openrouter.ai/api/v1"` ile `openai.OpenAI` istemcisi yapılandırılır
- `api_key` yalnızca `config.py` üzerinden gelir; sabit kodlanmaz
- Model adı `config.py` üzerinden okunur; `analyzer.py` içinde model adı sabit yazılmaz
