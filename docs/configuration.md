# Configuration

## Çoklu Sağlayıcı Kurulum

Bu proje AI çağrıları için OpenRouter veya DeepSeek kullanacak şekilde yapılandırılabilir. Her iki servis de OpenAI uyumlu API sunduğu için mevcut istemci yapısı korunur.

## `.env` Dosyası

Proje yapılandırması `.env` dosyası üzerinden yüklenir. Aşağıdaki örnek temel ayarları gösterir:

```env
LLM_PROVIDER=openrouter

OPENROUTER_API_KEY=sk-or-...
ANALYSIS_PROMPT="Sen kıdemli bir Ürün Yöneticisi ve Pazar Araştırma Stratejistisin..."
OPENROUTER_MODEL="nvidia/nemotron-3-super:free"
DATABASE_PATH=analiz_gecmisi.db

# DeepSeek seçilirse
# DEEPSEEK_API_KEY=sk-...
# DEEPSEEK_MODEL=deepseek-v4-flash
# DEEPSEEK_THINKING_ENABLED=true
# DEEPSEEK_REASONING_EFFORT=high

# Aşama 2 — Opportunity Map
OPPORTUNITY_MAP_PROMPT="Sen kıdemli bir SaaS Growth Stratejisti ve Fırsat Analistisisin..."

# Aşama 3 — Master LLM Prompt Sentezi
SYNTHESIS_PROMPT="Sen bir AI Ürün Stratejisti ve Prompt Mimarısısın..."
```

## Önemli Değişkenler

- `LLM_PROVIDER`
  - `openrouter` veya `deepseek`.
  - Varsayılan `openrouter`.
- `OPENROUTER_API_KEY`
  - `LLM_PROVIDER=openrouter` iken gereklidir.
- `ANALYSIS_PROMPT`
  - AI analizinin nasıl çalışacağını belirler.
  - Özelleştirilerek farklı analiz çerçeveleri kullanılabilir.
- `OPENROUTER_MODEL`
  - OpenRouter tarafında kullanılacak model adını belirler.
  - Önerilen değer: `nvidia/nemotron-3-super:free`
- `DEEPSEEK_API_KEY`
  - `LLM_PROVIDER=deepseek` iken gereklidir.
- `DEEPSEEK_MODEL`
  - DeepSeek modeli.
  - Resmi yeni modeller: `deepseek-v4-flash`, `deepseek-v4-pro`.
  - Geçiş için eski eşlemeler desteklenir: `deepseek-chat`, `deepseek-reasoner`.
- `DEEPSEEK_THINKING_ENABLED`
  - DeepSeek düşünme modunu açar veya kapatır.
  - Varsayılan: `true`.
- `DEEPSEEK_REASONING_EFFORT`
  - Düşünme yoğunluğu.
  - Geçerli değerler: `high`, `max`.
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

## Önerilen Modeller

### OpenRouter

- `nvidia/nemotron-3-super:free` - en güçlü stratejik analiz tercihi.
- `tencent/hy3-preview:free` - yapılandırılabilir derinlik için güçlü alternatif.
- `qwen/qwen3-next-80b-a3-instruct:free` - dengeli performans.
- `openai/gpt-oss-120b:free` - genel amaçlı yüksek performans.
- `google/gemma-4-31b:free` - çok dilli yorum analizleri için uygun.

### DeepSeek

- `deepseek-v4-flash` - varsayılan ve genel kullanım için önerilen model.
- `deepseek-v4-pro` - daha ağır analiz ve daha yüksek kalite için alternatif.
- `deepseek-chat` - geçiş süresince non-thinking alias.
- `deepseek-reasoner` - geçiş süresince thinking alias.

## Ek Ayarlar

Eğer `config.py` başka değişkenler yüklüyorsa, bu değişkenleri de `.env` içinde tanımlayın. Örnek:

```env
LOG_LEVEL=INFO
DEFAULT_STORE=android
```

## OpenAI Uyumlu İstemci Ayarı

- OpenRouter kullanırken istemci `base_url` değeri `https://openrouter.ai/api/v1` olmalıdır.
- DeepSeek kullanırken istemci `base_url` değeri `https://api.deepseek.com` olmalıdır.
- DeepSeek için düşünme modu `thinking: { type: "enabled" }` ve `reasoning_effort` alanlarıyla kontrol edilir.

## Değişiklik Uygulama

`.env` dosyasını değiştirdikten sonra projenin yeniden başlatılması yeterlidir. Değişiklikler `main.py` çalıştırıldığında otomatik olarak okunur.
