# Configuration

## OpenRouter Odaklı Kurulum

Bu proje AI çağrıları için OpenRouter kullanacak şekilde yapılandırılabilir. OpenRouter, OpenAI uyumlu API sunduğu için mevcut istemci yapısı korunarak ücretsiz modeller seçilebilir.

## `.env` Dosyası

Proje yapılandırması `.env` dosyası üzerinden yüklenir. Aşağıdaki örnek temel ayarları gösterir:

```env
OPENROUTER_API_KEY=sk-or-...
ANALYSIS_PROMPT="Sen kıdemli bir Ürün Yöneticisi ve Pazar Araştırma Stratejistisin..."
OPENROUTER_MODEL="nvidia/nemotron-3-super:free"
DATABASE_PATH=analiz_gecmisi.db

# Aşama 2 — Opportunity Map
OPPORTUNITY_MAP_PROMPT="Sen kıdemli bir SaaS Growth Stratejisti ve Fırsat Analistisisin..."

# Aşama 3 — Master LLM Prompt Sentezi
SYNTHESIS_PROMPT="Sen bir AI Ürün Stratejisti ve Prompt Mimarısısın..."
```

## Önemli Değişkenler

- `OPENROUTER_API_KEY`
  - OpenRouter üzerindeki ücretsiz veya ücretli modellere erişim için gereklidir.
- `ANALYSIS_PROMPT`
  - AI analizinin nasıl çalışacağını belirler.
  - Özelleştirilerek farklı analiz çerçeveleri kullanılabilir.
- `OPENROUTER_MODEL`
  - Kullanılacak model adını belirler.
  - Önerilen değer: `nvidia/nemotron-3-super:free`
- `DATABASE_PATH`
  - SQLite veritabanı dosya yolu.
  - Varsayılan olarak `analiz_gecmisi.db` kullanılır.
- `OPPORTUNITY_MAP_PROMPT`
  - Aşama 2'de fırsat haritası üretmek için kullanılan sistem prompt'u.
  - Tanımlanmazsa `config.py` içindeki varsayılan şablon devreye girer.
  - Detaylı prompt yapısı: `docs/opportunity-map.md`
- `SYNTHESIS_PROMPT`
  - Aşama 3'te frontier modeller için master prompt oluşturmak amacıyla kullanılır.
  - Tanımlanmazsa `config.py` içindeki varsayılan şablon devreye girer.
  - Detaylı prompt yapısı: `docs/master-prompt-synthesis.md`

## Önerilen Ücretsiz Modeller

- `nvidia/nemotron-3-super:free` - en güçlü stratejik analiz tercihi.
- `tencent/hy3-preview:free` - yapılandırılabilir derinlik için güçlü alternatif.
- `qwen/qwen3-next-80b-a3-instruct:free` - dengeli performans.
- `openai/gpt-oss-120b:free` - genel amaçlı yüksek performans.
- `google/gemma-4-31b:free` - çok dilli yorum analizleri için uygun.

Kısa veri kümelerinde veya hız öncelikli senaryolarda `liquid/lfm-2.5-1.2b-thinking:free` ve `qwen/qwen3-coder:free` gibi modeller de tercih edilebilir.

## Ek Ayarlar

Eğer `config.py` başka değişkenler yüklüyorsa, bu değişkenleri de `.env` içinde tanımlayın. Örnek:

```env
LOG_LEVEL=INFO
DEFAULT_STORE=android
```

## OpenAI Uyumlu İstemci Ayarı

OpenRouter kullanırken istemci `base_url` değeri `https://openrouter.ai/api/v1` olarak ayarlanmalıdır. Bu sayede standart OpenAI uyumlu çağrı biçimi korunur.

## Değişiklik Uygulama

`.env` dosyasını değiştirdikten sonra projenin yeniden başlatılması yeterlidir. Değişiklikler `main.py` çalıştırıldığında otomatik olarak okunur.
