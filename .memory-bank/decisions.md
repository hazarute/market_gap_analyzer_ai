# Decisions

## Is Kurallari

- **Tekrar Analiz Yok:** Aynı `app_id` (uygulama paket adı veya store kimliği) bir kez analiz edilirse, `analiz_gecmisi` tablosundaki kayıt nedeniyle ikinci kez LLM çağrısı yapılmaz. Bu kural hem maliyet kontrolü hem de API kotası yönetimi için değişmezdir.
- **Gizli Veri .env'de:** `OPENROUTER_API_KEY` ve diğer hassas değerler yalnızca `.env` dosyasında yaşar. Kaynak koda, talimat dosyalarına veya memory bank'e asla yazılmaz.
- **Prompt Dışarıdan Yönetilir:** `ANALYSIS_PROMPT`, `OPPORTUNITY_MAP_PROMPT` ve `SYNTHESIS_PROMPT` değişkenleri `.env` üzerinden kontrol edilir. Tanımlanmayan isteğe bağlı promptlar için ilgili modüldeki varsayılan şablon devreye girer.
- **LLM Sağlayıcı Soyutlaması:** LLM çağrıları `LLM_PROVIDER` ile seçilen sağlayıcı üzerinden yapılır. OpenRouter için endpoint `https://openrouter.ai/api/v1`, DeepSeek için `https://api.deepseek.com` kullanılır. Model ve düşünme ayarları `config.py` içinde normalize edilir.
- **DeepSeek v4 Varsayılanı:** DeepSeek tarafında varsayılan model `deepseek-v4-flash`'tir. Eski `deepseek-chat` ve `deepseek-reasoner` alias'ları geçiş süresince `deepseek-v4-flash`'e eşlenir.
- **Thinking Modu:** DeepSeek çağrılarında `thinking: { type: "enabled" }` ve `reasoning_effort` desteklenir. Düşünme modu `.env` üzerinden kapatılabilir.
- **Çoklu Mağaza Araması:** `--store` CLI argümanı bir veya daha fazla mağaza alabilir. Seçilen mağazalar sırayla taranır; Android ve iOS aynı çalışmada birlikte işlenebilir.
- **Otomatik Batch İlerlemesi:** `--page` argümanı kaldırıldı. `_fetch_new_apps()` fonksiyonu her çalıştırmada DB'yi kontrol ederek analiz edilmiş uygulamaları atlar ve tam `--limit` kadar yeni uygulama bulunana kadar otomatik olarak sonraki batch'lere (offset artırarak) ilerler. Kullanıcıdan herhangi bir sayfalama parametresi beklenmez.
- **Markdown Rapor Formatı:** Analiz çıktıları `rapor_<uygulama_adi>.md` formatında kaydedilir. Fırsat haritaları `opportunity_map_<uygulama_adi>.md`, master promptlar `master_prompt_<uygulama_adi>.md` formatında `reports/` klasörüne eklenir.
- **İki Platform:** Google Play (`android`) ve Apple App Store (`ios`) desteklenir. Yeni mağaza desteği `scrapers/` altına bağımsız modül eklenerek yapılır.

## Mimari Kararlar (ADR)

### ADR-001: SQLite Seçimi
- **Tarih:** Proje başlangıcı
- **Karar:** Analiz geçmişi için SQLite kullanılır.
- **Gerekçe:** Dış bağımlılık gerektirmez, kurulum sıfır, tek kullanıcılı senaryo için yeterlidir.
- **Etki:** `analiz_gecmisi.db` proje kökünde oluşturulur; `.gitignore`'a eklenmesi zorunludur.

### ADR-002: OpenRouter ile OpenAI Uyumlu İstemci
- **Tarih:** Proje başlangıcı
- **Karar:** `openai` Python kütüphanesi, `base_url=https://openrouter.ai/api/v1` ile kullanılır.
- **Gerekçe:** OpenRouter ücretsiz modellere erişim sağlar; standart OpenAI istemcisi kullanarak vendor lock-in azaltılır.
- **Etki:** Model değişikliği yalnızca `.env` değişkeni güncellenmesiyle yapılabilir.

### ADR-003: Pipeline Tasarımı (3 Aşamalı)
- **Tarih:** v1.1 — 2026-05-14
- **Karar:** Pipeline, birbirini besleyen 3 aşamaya ayrılmıştır: (1) Rakip Analizi, (2) Opportunity Map, (3) Master LLM Prompt Sentezi.
- **Gerekçe:** Her aşama bağımsız çalıştırılabilir; Aşama 2 ve 3 isteğe bağlı CLI bayraklarıyla (`--opportunity-map`, `--master-prompt`, `--all-stages`) etkinleştirilir. Geriye dönük uyumluluk korunur.
- **Etki:** `main.py` koordinatör rolünü genişletti; `opportunity_mapper.py` ve `prompt_synthesizer.py` eklendi.

### ADR-004: Scraper Katmanı Bağımsızlığı
- **Tarih:** Proje başlangıcı
- **Karar:** `scrapers/` modülleri analiz yapmaz; yalnızca veri toplar.
- **Gerekçe:** Tek Sorumluluk Prensibi (SRP). Mağaza API'si değişirse yalnızca scraper güncellenir.
- **Etki:** Scraper çıktısı standart sözlük yapısı (`app_id`, `app_name`, `store`, `score`, `description`) döndürmelidir.

### ADR-005: LangChain LCEL Kullanımı
- **Tarih:** v1.1 — 2026-05-14
- **Karar:** Aşama 2 ve 3'te LangChain LCEL (`prompt | llm | StrOutputParser()`) zinciri kullanılır. `langchain-community` bağımlılığı eklenmedi; dosya okuma `pathlib.Path.read_text()` ile yapılır.
- **Gerekçe:** LCEL modern ve önerilen LangChain API'sidir; `LLMChain` deprecated. `langchain-community` ağır bir bağımlılık olduğundan minimumda tutuldu.
- **Etki:** `requirements.txt` içine `langchain>=0.3.0` ve `langchain-openai>=0.2.0` eklendi.

### ADR-006: Otomatik Batch İlerlemesi
- **Tarih:** v1.2 — 2026-05-16
- **Karar:** Manuel `--page` argümanı kaldırıldı; `_fetch_new_apps()` yardımcı fonksiyonu eklendi. Fonksiyon `limit` büyüklüğünde batch'ler halinde arama yapar, her app'i DB'ye karşı filtreler ve tam `limit` yeni uygulama bulunana ya da sonuçlar tükenene kadar `offset += limit` ile ilerler.
- **Gerekçe:** Kullanıcının hangi batch'te olduğunu takip etmesi gerekmemelidir. Aynı anahtar kelimeyle tekrar çalıştırılan komut her zaman yeni uygulamalara ilerler. Farklı anahtar kelimelerden DB'ye düşen uygulamalar da otomatik atlanır.
- **Etki:** `main.py` içinde `_fetch_new_apps()` fonksiyonu; scraper'lar `offset` parametresi alıyor. Güvenlik sınırı olarak `max_total_fetch = limit * 20` uygulandı (sonsuz döngü koruması).

## Gecici Cozumler ve Operasyonel Notlar

- `requirements.txt` henüz oluşturulmamıştır; README'den türetilecek bağımlılıklar: `google-play-scraper`, `app-store-scraper`, `openai`, `python-dotenv`.
- `analiz_gecmisi.db` ve `rapor_*.md` dosyaları `.gitignore`'a eklenmelidir (henüz `.gitignore` oluşturulmamıştır).
- CLI parametreleri: `--keyword`, `--store`, `--limit` (varsayılan: 10) mevcut ve çalışıyor.

## Mevcut Risk Kaydi

- **Scraper Kırılganlığı:** `google-play-scraper` ve `app-store-scraper` üçüncü taraf kütüphanelerdir; mağaza API yapısı değişirse scraper'lar güncellenmelidir.
- **OpenRouter Ücretsiz Model Sınırları:** Ücretsiz modellerin rate limit ve bağlam penceresi kısıtlamaları analizin derinliğini etkileyebilir.
- **DeepSeek Geçiş Riski:** `deepseek-chat` ve `deepseek-reasoner` alias'ları deprecation takvimine bağlıdır; üretimde `deepseek-v4-flash` ve `deepseek-v4-pro` tercih edilmelidir.
- **Büyük Veri Seti Yönetimi:** Çok sayıda uygulama analiz edildiğinde API istek süresi uzayabilir; gelecekte asenkron işleme veya batch analiz gerekebilir.
- **Prompt Kalitesi:** `ANALYSIS_PROMPT` değişkeninin içeriği doğrudan rapor kalitesini belirler; yetersiz prompt düşük kaliteli çıktıya yol açar.
