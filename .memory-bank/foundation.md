# Foundation

## Proje Ozeti

Market Gap Analyzer AI, Google Play Store ve Apple App Store'daki sektör lideri uygulamaları tersine mühendislik ile analiz eden, yapay zeka destekli bir stratejik pazar araştırması otomasyonudur. OpenRouter veya DeepSeek API üzerinden çalışan LLM modellerini kullanarak kıdemli bir ürün yöneticisi bakış açısıyla pazar boşluklarını, kullanıcı sürtünmelerini (friction) ve niş SaaS fırsatlarını `.md` formatında raporlar. 3 aşamalı pipeline ile (1) rakip analizi, (2) fırsat haritası (LangChain) ve (3) frontier LLM'lere hazır master prompt sentezi üretir.

## Teknoloji Yigini

**Backend / Uygulama Çekirdeği:**
- Python 3.10+
- `google-play-scraper` — Google Play Store scraper kütüphanesi
- `app-store-scraper` — Apple App Store scraper kütüphanesi
- `openai` — OpenRouter veya DeepSeek ile OpenAI uyumlu istemci (`base_url` sağlayıcıya göre değişir)
- `langchain>=0.3.0` + `langchain-openai>=0.2.0` — Aşama 2 ve 3 için LCEL zinciri
- `python-dotenv` — `.env` tabanlı yapılandırma yönetimi
- `argparse` (standart kütüphane) — CLI parametreleri

**Veritabanı:**
- SQLite (`analiz_gecmisi.db`) — analiz geçmişi, rapor yolları, fırsat haritası ve master prompt yollarını tutar

**AI / LLM:**
- OpenRouter API (OpenAI uyumlu endpoint)
- DeepSeek API (OpenAI uyumlu endpoint, `thinking` ve `reasoning_effort` destekli)
- Öncelikli OpenRouter model: `nvidia/nemotron-3-super:free`
- Öncelikli DeepSeek model: `deepseek-v4-flash`
- Alternatifler: `tencent/hy3-preview:free`, `qwen/qwen3-next-80b-a3-instruct:free`, `openai/gpt-oss-120b:free`, `google/gemma-4-31b:free`, `deepseek-v4-pro`

**Yapılandırma:**
- `.env` dosyası — `LLM_PROVIDER`, `OPENROUTER_API_KEY` veya `DEEPSEEK_API_KEY`, `ANALYSIS_PROMPT`, `OPENROUTER_MODEL` veya `DEEPSEEK_MODEL`, `DATABASE_PATH`
- Opsiyonel: `DEEPSEEK_THINKING_ENABLED`, `DEEPSEEK_REASONING_EFFORT`, `OPPORTUNITY_MAP_PROMPT`, `SYNTHESIS_PROMPT` (tanımlanmazsa modül içi varsayılan kullanılır)
- `config.py` — `.env` değişkenlerini uygulamaya aktarır

**Çıktı:**
- Aşama 1: `reports/rapor_<uygulama_adi>.md` — rakip analizi
- Aşama 2: `reports/opportunity_map_<uygulama_adi>.md` — fırsat haritası
- Aşama 3: `reports/master_prompt_<uygulama_adi>.md` — frontier LLM için hazır prompt

**Bağımlılık Dosyası:**
- `requirements.txt`

## Sistem Mimarisi

Proje, 3 aşamalı tek yönlü bir pipeline olarak çalışır:

```
Kullanıcı CLI (main.py)
    ↓
Scraper Katmanı (scrapers/google_play.py | scrapers/app_store.py)
    ↓
Veritabanı Kontrol (database.py) — zaten analiz edildiyse atla
    ↓
LLM Analiz (analyzer.py) — OpenRouter + ANALYSIS_PROMPT
    ↓
Rapor Üretimi (report_generator.py) — reports/rapor_<app>.md   [Aşama 1]
    ↓ (--opportunity-map veya --all-stages)
Fırsat Haritası (opportunity_mapper.py) — LangChain LCEL + OPPORTUNITY_MAP_PROMPT
    → reports/opportunity_map_<app>.md                          [Aşama 2]
    ↓ (--master-prompt veya --all-stages)
Master Prompt Sentezi (prompt_synthesizer.py) — LangChain LCEL + SYNTHESIS_PROMPT
    → reports/master_prompt_<app>.md                            [Aşama 3]
    ↓
Veritabanı Kayıt (database.py) — analiz_gecmisi.db
```

**Sorumluluk Sınırları:**
- `scrapers/` → yalnızca mağaza verisi toplar; analiz yapmaz
- `database.py` → analiz geçmişi kontrolü ve kayıt
- `analyzer.py` → prompt yönetimi ve LLM çağrı orkestrasyonu (OpenRouter veya DeepSeek)
- `report_generator.py` → AI çıktısını kullanıcı dostu Markdown'a çevirir
- `opportunity_mapper.py` → rapor_*.md'yi LangChain ile işleyerek fırsat haritası üretir
- `prompt_synthesizer.py` → iki raporu LangChain ile sentezleyerek master prompt üretir
- `config.py` → `.env` değerlerini uygulama katmanına aktarır

## Klasor Yapisi

```
.
├── main.py                    # Ana CLI betiği (keyword, store, aşama bayrakları)
├── scrapers/
│   ├── google_play.py         # Google Play scraper
│   └── app_store.py           # App Store scraper
├── database.py                # SQLite bağlantısı + analiz_gecmisi tablosu
├── analyzer.py                # LLM analizi (OpenRouter + ANALYSIS_PROMPT)
├── report_generator.py        # Markdown rapor üretimi (Aşama 1)
├── opportunity_mapper.py      # LangChain LCEL — fırsat haritası (Aşama 2)
├── prompt_synthesizer.py      # LangChain LCEL — master prompt sentezi (Aşama 3)
├── config.py                  # .env yükleyici
├── requirements.txt           # Python bağımlılıkları
├── version.txt                # Sürüm geçmişi ve notlar
├── .env                       # Gizli yapılandırma (git'e eklenmez)
├── .env.example               # Şablon yapılandırma
├── analiz_gecmisi.db          # SQLite veritabanı (git'e eklenmez)
├── reports/
│   ├── rapor_*.md             # Aşama 1 çıktıları
│   ├── opportunity_map_*.md   # Aşama 2 çıktıları
│   └── master_prompt_*.md     # Aşama 3 çıktıları
├── docs/                      # Teknik dokümantasyon
└── .github/                   # AI asistan yapılandırmaları
```

## Urun ve Mimari Odaklar

- **Tekrar Önleme:** Aynı `app_id` bir kez analiz edilir; SQLite bu kaydı tutar.
- **Prompt Özelleştirme:** `ANALYSIS_PROMPT`, `OPPORTUNITY_MAP_PROMPT`, `SYNTHESIS_PROMPT` değişkenleri ile tüm aşamaların analiz çerçevesi özelleştirilebilir.
- **Mağaza Bağımsızlığı:** `--store android`, `--store ios` veya `--store android ios` ile iki platform aynı çalışmada taranabilir.
- **Model Esnekliği:** `LLM_PROVIDER` ile OpenRouter veya DeepSeek seçilebilir; model ve thinking ayarları `.env` değişkenleriyle değiştirilebilir.
- **Çıktı Taşınabilirliği:** Raporlar `.md` formatında üretilir; Notion, Obsidian ve GitHub ile doğrudan kullanılabilir.
- **Pipeline Esnekliği:** Aşama 2 ve 3 isteğe bağlıdır; yalnızca `--opportunity-map`, `--master-prompt` veya `--all-stages` bayrağıyla etkinleştirilir.
