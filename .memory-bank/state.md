# State

## Mevcut Odak

**v1.1 tamamlandı ve kapatıldı.** 3 aşamalı pipeline uygulandı: LangChain ile Opportunity Map (Aşama 2) ve Master LLM Prompt Sentezi (Aşama 3) eklendi. 33 birim testi geçiyor. `.env.example` (Aşama 2+3 prompt değişkenleri) ve `version.txt` (yapılandırılmış sürüm notları formatı) güncellendi. Gerçek API anahtarıyla uçtan uca pipeline doğrulaması için `.env` dosyası oluşturup şu komutları kullanın:

```bash
# Yalnızca Aşama 1 (mevcut davranış):
python main.py --keyword "<anahtar_kelime>" --store android

# Tam pipeline (3 aşama):
python main.py --keyword "<anahtar_kelime>" --store android --all-stages
```

## Aktif Faz

- Faz 0 - Dokümantasyon ve Memory Bank Kurulumu : [x]
- Faz 1 - Temel Python Modülleri : [x]
- Faz 2 - Scraper Katmanı : [x]
- Faz 3 - Veritabanı ve Analiz Pipeline'ı : [x]
- Faz 4 - Test ve Doğrulama : [x]
- Faz 5 - LangChain Entegrasyonu (v1.1) : [x]

## Gorev Listesi

### Faz 1 - Temel Python Modülleri

Referans dokumanlar:
- `../README.md`
- `../docs/architecture.md`
- `../docs/configuration.md`

#### Faz 1 amaci
- Projenin çalışabilir iskeletini oluşturmak: `config.py`, temel `main.py` CLI yapısı, `requirements.txt` ve `.env.example` dosyalarını hayata geçirmek.

#### Faz 1 cikis kriterleri
- `python main.py --keyword "test" --store android` komutu çalışıp hata vermeden pipeline akışını başlatabilmeli.
- `config.py` `.env` değerlerini doğru yüklemeli.
- `requirements.txt` içinde gerekli bağımlılıklar listelenmiş olmalı.

#### 1. Yapılandırma katmanını oluştur
Ref: `../docs/configuration.md`
- [x] `.env.example` dosyasını oluştur (`OPENROUTER_API_KEY`, `ANALYSIS_PROMPT`, `OPENROUTER_MODEL`, `DATABASE_PATH`)
- [x] `config.py` modülünü oluştur (`python-dotenv` ile `.env` yükleyici)
- [x] `requirements.txt` dosyasını oluştur

#### 2. CLI girişini oluştur
Ref: `../README.md`, `../docs/architecture.md`
- [x] `main.py` temel iskeletini oluştur (`--keyword` ve `--store` argparse parametreleri ile)
- [x] Modül bağlantılarını (scraper, db, analyzer, report) iskelet halinde yerleştir

### Faz 2 - Scraper Katmanı

Referans dokumanlar:
- `../docs/scrapers.md`

#### Faz 2 amaci
- Google Play ve App Store scraper modüllerini çalışır hale getirmek.

#### Faz 2 cikis kriterleri
- `scrapers/google_play.py` verilen anahtar kelime için uygulama listesi döndürmeli.
- `scrapers/app_store.py` verilen anahtar kelime için uygulama listesi döndürmeli.
- Her iki modül standart çıktı yapısını (`app_id`, `app_name`, `store`, `score`, `description`) üretmeli.

#### 3. Google Play scraper modülünü oluştur
Ref: `../docs/scrapers.md`
- [x] `scrapers/__init__.py` oluştur
- [x] `scrapers/google_play.py` içinde anahtar kelime bazlı arama fonksiyonu oluştur
- [x] Uygulama detay çekme fonksiyonu ekle

#### 4. App Store scraper modülünü oluştur
Ref: `../docs/scrapers.md`
- [x] `scrapers/app_store.py` içinde anahtar kelime bazlı arama fonksiyonu oluştur
- [x] Uygulama detay çekme fonksiyonu ekle

### Faz 3 - Veritabanı ve Analiz Pipeline'ı

Referans dokumanlar:
- `../docs/database-schema.md`
- `../docs/prompt-guidelines.md`
- `../docs/architecture.md`

#### Faz 3 amaci
- SQLite entegrasyonu, LLM analiz katmanı ve Markdown rapor üretimini tamamlamak.

#### Faz 3 cikis kriterleri
- `database.py` `analiz_gecmisi` tablosunu otomatik oluşturmalı ve tekrar analiz engelini sağlamalı.
- `analyzer.py` OpenRouter üzerinden LLM çağrısı yapabilmeli.
- `report_generator.py` `rapor_<app_name>.md` üretebilmeli.

#### 5. Veritabanı katmanını oluştur
Ref: `../docs/database-schema.md`
- [x] `database.py` modülünü oluştur
- [x] `analiz_gecmisi` tablosunu otomatik oluşturan `init_db()` fonksiyonu ekle
- [x] `is_analyzed(app_id)` kontrol fonksiyonu ekle
- [x] `save_analysis(...)` kayıt fonksiyonu ekle

#### 6. Analyzer modülünü oluştur
Ref: `../docs/prompt-guidelines.md`, `../README.md`
- [x] `analyzer.py` modülünü oluştur
- [x] OpenRouter OpenAI uyumlu istemciyi yapılandır
- [x] `analyze_app(app_data)` fonksiyonunu oluştur

#### 7. Rapor üretecini oluştur
- [x] `report_generator.py` modülünü oluştur
- [x] `generate_report(app_name, analysis_result)` fonksiyonunu oluştur
- [x] Çıktı dosyasını `rapor_<app_name>.md` formatında kaydet

### Faz 4 - Test ve Doğrulama

Referans dokumanlar:
- `../docs/usage.md`

#### Faz 4 amaci
- Uçtan uca pipeline'ın çalıştığını doğrulamak.

#### Faz 4 cikis kriterleri
- Gerçek bir anahtar kelimeyle `main.py` çalıştırıldığında en az bir rapor üretilmeli.
- Aynı uygulama ikinci kez çalıştırıldığında tekrar analiz edilmemeli.

#### 8. Uçtan uca testi gerçekleştir
- [x] Birim testleri oluştur (`tests/test_database.py`, `tests/test_report_generator.py`)
- [x] 12 birim testi çalıştırıldı ve geçti (pytest 9.0.3, Python 3.14.4)
- [x] Veritabanı kaydı ve tekrar analiz engeli birim testlerle doğrulandı
- [x] Rapor formatı ve dosya adı üretimi birim testlerle doğrulandı
- [x] Gerçek API anahtarıyla uçtan uca doğrulama — TAMAMLANDI (14 Mayıs 2026)

## Durum Notlari

- `.memory-bank/` klasörü BAŞLAT akışıyla oluşturuldu (14 Mayıs 2026).
- Faz 1 tamamlandı (14 Mayıs 2026): `config.py`, `main.py`, `requirements.txt`, `.env.example`, `.gitignore` oluşturuldu.
- Faz 2 tamamlandı (14 Mayıs 2026): `scrapers/__init__.py`, `scrapers/google_play.py`, `scrapers/app_store.py` oluşturuldu.
- Faz 3 tamamlandı (14 Mayıs 2026): `database.py`, `analyzer.py`, `report_generator.py` oluşturuldu.
- Faz 4 tamamlandı (14 Mayıs 2026): 12 birim testi geçti; `datetime.utcnow()` deprecation uyarısı `datetime.now(timezone.utc)` ile düzeltildi.
- Uçtan uca doğrulama TAMAMLANDI (14 Mayıs 2026): `deepseek/deepseek-v4-flash:free` modeli ile "Meditasyon" anahtar kelimesiyle Android mağazasında 2 uygulama analiz edildi. Raporlar oluşturuldu, SQLite'a kaydedildi, deduplication doğrulandı.
- `requests<2.28` `requirements.txt`'e eklendi (`app-store-scraper` uyumluluğu için zorunlu).
- Geçerli çalışan model: `deepseek/deepseek-v4-flash:free` (~2 dak/analiz). `meta-llama/llama-3.3-70b-instruct:free` Venice sağlayıcı rate-limit'i yaşıyor.
- Pipeline eksiksiz; `main.py` tüm modülleri orkestrasyonlu olarak bağlamaktadır.
- `analyzer.py` içindeki `_MAX_REVIEW_CHARS` (3000) ve `_MAX_DESC_CHARS` (2000) sabitleri LLM bağlam penceresi aşımını önlemek için kullanılmaktadır.
- `app-store-scraper` keyword arama desteği sınırlıdır; iOS aramaşı uygulama adı üzerinden çalışmaktadır (karar ADR-004 kapsamında tutuldu).
- `main.py` tam pipeline orkestrasyonunu içeriyor; Faz 2 scraper modülleri tamamlanınca çalışır hale gelecek.
- `requirements.txt` içindeki sürümler (`google-play-scraper==1.2.7`, `app-store-scraper==0.3.5`) README'den türetilmiştir; kurulumda güncel sürümler kontrol edilmelidir.
