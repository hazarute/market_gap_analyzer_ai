# Architecture

## Overview

Market Gap Analyzer AI, mobil uygulama mağazası verilerini tarayan, geçmiş analizleri kaydeden ve yapay zeka destekli pazar raporları üreten bir Python otomasyonudur.

## Bileşenler

- `main.py`
  - CLI parametrelerini alır
  - `scrapers`, `database`, `analyzer`, `report_generator`, `opportunity_mapper`, `prompt_synthesizer` modüllerini yönetir
  - `--opportunity-map` ve `--master-prompt` bayraklarıyla Aşama 2 ve Aşama 3'ü etkinleştirir
- `scrapers/`
  - `google_play.py`
  - `app_store.py`
  - Mağazalardan uygulama ve kullanıcı verisi çeker
- `database.py`
  - SQLite bağlantısı sağlar
  - Analiz geçmişini, rapor yollarını, fırsat haritası ve master prompt yollarını saklar
- `analyzer.py`
  - Uygulama verisini prompt ile AI analizine dönüştürür
  - OpenRouter uyumlu OpenAI istemcisi ile model çağrısı yapar
  - `ANALYSIS_PROMPT` değişkenini kullanır
- `report_generator.py`
  - AI çıktısını Markdown raporuna çevirir
  - `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` formatında dosya üretir
- `opportunity_mapper.py` *(Aşama 2 — Yeni)*
  - `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` dosyasını doğrudan okur
  - `PromptTemplate`, `ChatOpenAI` ve `StrOutputParser()` kullanarak OpenRouter çağrısı yapar
  - `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` olarak kaydeder
  - Detay: `docs/opportunity-map.md`
- `prompt_synthesizer.py` *(Aşama 3 — Yeni)*
  - `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` ve `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` dosyalarını birleştirir
  - `PromptTemplate`, `ChatOpenAI` ve `StrOutputParser()` kullanarak frontier LLM prompt'u üretir
  - `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md` olarak kaydeder
  - Detay: `docs/master-prompt-synthesis.md`
- `config.py`
  - `.env` dosyasını okur
  - ortam değişkenlerini uygulamaya aktarır

## Veri Akışı

### Aşama 1 — Rakip Analizi (Mevcut)

1. Kullanıcı `main.py` ile arama anahtarı ve mağaza seçer.
2. `scrapers/` ilgili mağazadan uygulama listesini alır.
3. `database.py`, aynı uygulamanın önceden analiz edilip edilmediğini kontrol eder.
4. Yeni uygulamalar için `analyzer.py` LLM çağrısı yapar.
5. `report_generator.py` raporu `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` olarak kaydeder.
6. `database.py` analiz geçmişini ve rapor yolunu veritabanına yazar.

### Aşama 2 — Opportunity Map (Yeni)

7. `opportunity_mapper.py`, `reports/<uygulama_adi>/rapor_<uygulama_adi>.md` dosyasını doğrudan okur.
8. `PromptTemplate`, `ChatOpenAI` ve `StrOutputParser()` ile OpenRouter çağrısı yapılır.
9. Çıktı `reports/<uygulama_adi>/opportunity_map_<uygulama_adi>.md` olarak kaydedilir.
10. `database.py`, `opportunity_map_path` ve `opportunity_map_at` alanlarını günceller.

### Aşama 3 — Master LLM Prompt Sentezi (Yeni)

11. `prompt_synthesizer.py`, `rapor_*.md` ve `opportunity_map_*.md` dosyalarını okur.
12. `SYNTHESIS_PROMPT` şablonuyla her iki belge birleştirilip AI'ya gönderilir.
13. Çıktı `reports/<uygulama_adi>/master_prompt_<uygulama_adi>.md` olarak kaydedilir; frontier modellere yapıştırmaya hazır.
14. `database.py`, `master_prompt_path` ve `master_prompt_at` alanlarını günceller.

## Sınırlar ve Sorumluluklar

- `scrapers/` yalnızca açık kaynaklı, mağaza arama verisini toplar.
- `analyzer.py` prompt yönetimi ve model çağrı orkestrasyonundan sorumludur.
- `analyzer.py` model sağlayıcısı olarak OpenRouter uyumlu OpenAI istemcisini kullanır; istemci yapılandırması `config.py` üzerinden yönetilir.
- `report_generator.py` analiz sonucunu son kullanıcı dostu Markdown formatına dönüştürür.
- `opportunity_mapper.py` yalnızca mevcut `rapor_*.md` üzerinden çalışır; mağaza verisine doğrudan erişmez.
- `prompt_synthesizer.py` yalnızca Aşama 1 ve Aşama 2 çıktılarını tüketir; kendi başına scraping veya analiz yapmaz.

## Genişletilebilirlik

- Yeni mağaza scraper'ları eklemek için `scrapers/` altına modül ekleyin.
- Alternatif LLM'ler eklemek için `analyzer.py` içinde model adını veya OpenRouter hesabındaki ücretsiz modeli değiştirin.
- Rapor şablonunu değiştirmek için `report_generator.py` güncelleyin.
- Opportunity Map prompt'unu özelleştirmek için `.env` içindeki `OPPORTUNITY_MAP_PROMPT` değişkenini güncelleyin.
- Master prompt çıktı formatını özelleştirmek için `.env` içindeki `SYNTHESIS_PROMPT` değişkenini güncelleyin.

## Bağımlılıklar

| Kütüphane | Kullanıldığı Modül | Amaç |
|-----------|--------------------|------|
| `openai` | `analyzer.py` | OpenRouter uyumlu LLM çağrısı |
| `langchain` | `opportunity_mapper.py`, `prompt_synthesizer.py` | LLM zinciri, prompt yönetimi, belge yükleme |
| `langchain-openai` | `opportunity_mapper.py`, `prompt_synthesizer.py` | LangChain için OpenAI / OpenRouter entegrasyonu |
| `google-play-scraper` | `scrapers/google_play.py` | Google Play veri toplama |
| `app-store-scraper` | `scrapers/app_store.py` | App Store veri toplama |
| `python-dotenv` | `config.py` | `.env` dosya okuma |
