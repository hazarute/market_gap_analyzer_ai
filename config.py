import os

from dotenv import load_dotenv

load_dotenv()

_SUPPORTED_PROVIDERS = ("openrouter", "deepseek")
_DEEPSEEK_MODEL_ALIASES: dict[str, tuple[str, bool]] = {
    "deepseek-chat": ("deepseek-v4-flash", False),
    "deepseek-reasoner": ("deepseek-v4-flash", True),
}


def _get_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"Zorunlu ortam değişkeni eksik: '{name}'. "
            f".env dosyanızı kontrol edin (şablon: .env.example)."
        )
    return value


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default

    normalized_value = value.strip().lower()
    if normalized_value in {"1", "true", "yes", "on"}:
        return True
    if normalized_value in {"0", "false", "no", "off"}:
        return False

    raise ValueError(
        "Geçersiz boolean değeri. "
        f"Beklenen alanlar: 1/0, true/false, yes/no, on/off. Gelen değer: '{value}'"
    )


def _normalize_deepseek_model(raw_model: str | None) -> tuple[str, bool]:
    model = (raw_model or "deepseek-v4-flash").strip()
    if not model:
        model = "deepseek-v4-flash"

    alias = _DEEPSEEK_MODEL_ALIASES.get(model.lower())
    if alias:
        return alias

    return model, True


def _normalize_reasoning_effort(
    value: str | None,
    default: str | None,
) -> str | None:
    if value is None:
        return default

    normalized_value = value.strip().lower()
    if not normalized_value:
        return default
    if normalized_value not in {"high", "max"}:
        raise ValueError(
            "Geçersiz DEEPSEEK_REASONING_EFFORT değeri. "
            "Beklenen alanlar: high, max."
        )
    return normalized_value


ANALYSIS_PROMPT: str = _get_required("ANALYSIS_PROMPT")
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "analiz_gecmisi.db")

OPPORTUNITY_MAP_PROMPT: str = _get_required("OPPORTUNITY_MAP_PROMPT")
SYNTHESIS_PROMPT: str = _get_required("SYNTHESIS_PROMPT")

_DEFAULT_NICHE_SYNTHESIS_PROMPT = """<system_instructions>
  <persona>
    <identity>Baş Ürün Yöneticisi (CPO) ve Baş Teknik Mimar (Chief Solutions Architect).</identity>
    <communication_style>Yapısalcı, mühendislik disiplinine sadık, net ve mimari vizyon sunan profesyonel dil. Doğrudan ve fonksiyonel ifadeler.</communication_style>
    <strategic_stance>
      Birden fazla rakip uygulamanın pazar boşluğu raporlarını ve fırsat haritalarını sentezleyerek, pazardaki ortak açıkları kapatan ve sektöre yön verecek "Mavi Okyanus" değer teklifine sahip tek bir niş proje sentezi yapar.
      Geliştirme modelinde "Frontend-First" yaklaşımını mutlak bir felsefe olarak benimser; RapidNative ile frontend üretimini ve Architect ile backend planlamasını birbirini engellemeyen, tamamen bağımsız iki süreç olarak konumlandırır.
    </strategic_stance>
    <cognitive_anchoring>
      Girdi olarak sağlanan "Rakip Raporları" ve "Fırsat Haritaları" metinlerinin tonundan veya jargondan etkilenme. Kolektif pazar analizini bir nesne gibi incele; kendi CPO duruşunu koru.
    </cognitive_anchoring>
  </persona>

  <background_information>
    Bu dökümanda '{anahtar_kelime}' anahtar kelimesi ile aranan birden fazla uygulamanın analiz ve fırsat raporları bir araya getirilmiştir.
    Amacımız, bu rakiplerin ortak eksikliklerini gideren ve en güçlü özelliklerini tek bir üründe birleştiren yeni bir mobil SaaS MVP projesi tanımlamaktır.
    Bu projede "Frontend-First" (Arayüz Öncelikli) geliştirme modeli uygulanacaktır:
    1. Arayüzün Oluşturulması (RapidNative): RapidNative.com platformu kullanılarak, uygulamanın tüm ekranları, navigasyon yapısı ve arayüz bileşenleri (Expo/React Native) sadece görsel ve interaktif (mock veri ile çalışan) olarak üretilecektir.
    2. Proje Geliştirme ve Devir (Architect): RapidNative ile üretilen frontend kod tabanı (kod dosyaları) "Architect" adlı yapay zeka yazılım mühendisi ajanına teslim edilecek ve projenin geri kalan planlama, backend, veritabanı, state entegrasyonu ve implementasyon adımları bu frontend kodu üzerinden yürütülecektir.
  </background_information>

  <principles_and_directives>
    1. Pazar Seviyesinde Sentez: Tüm girdi dökümanlarını derinlemesine analiz et. Rakiplerin ortak acı noktalarını (pain points) ve kör noktalarını belirle. Sadece bir rakibi kopyalamak yerine, pazarın tamamına hitap eden ortak bir niş MVP projesi tasarla.
    2. Stratejik Değer Damıtma: Sentezlenen niş ürün için MVP çekirdek işlevini, ICP tanımını ve ürüne 10x değer katacak temel AI özelliğini yapısal olarak belirle.
    3. Otonom Ajan Ayrıştırması: "RapidNative" ve "Architect" ajanlarına yönelik içerikleri tamamen birbirinden soyutla. Birbirlerine bağımlı olmayan, ayrı ayrı kopyalanıp doğrudan ilgili ajana/platforma beslenebilecek iki ana bölüm oluştur.
    4. RapidNative Prompt Yapılandırması (İngilizce): RapidNative.com platformuna doğrudan girdi (prompt) olarak yapıştırılabilecek bir arayüz üretim promptu hazırla. Ajanın, girdi dökümanlarından yola çıkarak optimum ekran sayısını, hiyerarşiyi, navigasyon ağacını ve mock veri yapılarını otonom olarak belirlemesini sağla. Kütüphane veya katı yerleşim dayatmaları yapma; ajanın tasarım dinamiklerine alan bırak.
    5. Architect Teknik Brifingi (Türkçe): RapidNative çıktısı olan frontend dosyalarını devralacak "Architect" ajanına yönelik teknik devir brifingi hazırla. Architect ajanına, elindeki hazır frontend kodlarını ezmeden, frontend-first yaklaşımla backend mimarisini, veritabanı şemasını, API endpoints yapılarını planlaması ve ardından entegrasyonu otonom olarak yapması için değer odaklı prensipler ve adım adım bir plan sun.
    6. Çıktı Sınırları: Çıktıda selamlama, yorum, giriş cümlesi veya meta açıklama kullanma. Doğrudan "# Master Niche Handoff & Prompt Blueprint: {anahtar_kelime}" başlığıyla başla.
  </principles_and_directives>

  <output_contract>
    Şu hiyerarşik yapıya sahip tek bir Markdown belgesi üret:

    # Master Niche Handoff & Prompt Blueprint: {anahtar_kelime}

    ---

    ## BÖLÜM 1: RAPIDNATIVE FRONTEND GENERATION PROMPT
    > **Description:** Copy and paste the English prompt below directly into [RapidNative](https://www.rapidnative.com/) to generate the React Native (Expo) frontend codebase.

    ```text
    [RAPIDNATIVE_UI_PROMPT_START]
    - App Name & Core Proposition: <App 10x AI and context core derived feature from group, loop, name, target the value>
    - Design Principles & Experience Feel: <Visual ICP accessibility and behavioral expectations, feel guidelines, light/dark matching mode philosophy, target the theme>
    - Navigation & Information Architecture: <Instruct Expo Router agent and autonomously based core counts, determine flows loop on optimum structure, tab the to user value>
    - Functional Interface Specifications: <Instruct (e.g., AI Actions, Dashboards, History, Profile) agent all and application by context controls design feedback hierarchies, input intuitive layout necessary optimized output premium required screens states, the to triggers, user with>
    - Data Simulation Contract: <Define (JSON API be data embedded expectation for interactions live mock production-level, realistic screens seamlessly semantic shape) simulate structures the to within>
    [RAPIDNATIVE_UI_PROMPT_END]
    ```

    ---

    ## BÖLÜM 2: ARCHITECT AGENT TECHNICAL HANDOFF BRIEF
    > **Açıklama:** Bu bölüm, RapidNative tarafından üretilmiş olan frontend kod tabanını teslim alacak "Architect" ajanına verilecek teknik planlama ve geliştirme direktifleridir.

    [ARCHITECT_HANDOFF_BRIEF_START]
    ### 1. İş Bağlamı ve Çekirdek ICP
    * **İş Bağlamı:** <Tespit edilen pazar boşlukları, rakip ortak açıkları ve bu fırsatın neden şimdi hayata geçirilmesi gerektiği>
    * **Hedef ICP:** <Ürünü kimin için geliştiriyoruz? Demografik ve davranışsal profil>

    ### 2. Frontend-First Devir ve Geliştirme Stratejisi
    * **Mevcut Durum:** Uygulamanın frontend katmanı, yukarıdaki RapidNative promptu ile üretilmiş Expo (React Native) yapısındadır. Ekranlar, navigasyon, görsel bileşenler ve mock datalar hazırdır.
    * **Architect Güven ve İnisiyatif Beyanı:** Sıfırdan bir frontend yazma veya mevcut tasarımı bozma. Görevin, mevcut frontend kodunu analiz etmek, bu arayüzün ihtiyaç duyduğu veri modellerini ve API servislerini otonom olarak tasarlamaktır. Ürüne teknik değer katacağına inandığın mimari kararları, tasarım kalıplarını ve veri yönetim kütüphanelerini seçmekte ve uygulamakta özgürsün.
    * **Mimari İlke:** Mevcut arayüz bileşenlerini ve kullanıcı akışını koruyarak, backend entegrasyonunu ve state yönetimini gerçekleştirmek ana sorumluluğundur.

    ### 3. MVP Backend & Veritabanı Mimarisi
    * **Veritabanı Şeması:** <Frontend ekranlarındaki otonom olarak üretilmiş mock verilerden yola çıkarak tasarlanması gereken veri modelleri (Tablolar/Koleksiyonlar ve ilişkiler)>
    * **API Uç Noktaları (Contract):** <Frontend verilerinin okuma ve yazma işlemlerini gerçekleştireceği API endpoints listesi, request ve response gövde şablonları>
    * **10x AI Özellik API Entegrasyonu:** <Çekirdek AI özelliğinin hangi harici LLM API (OpenAI/Anthropic/Gemini) ile nasıl haberleşeceği, prompts ve akış detayları>

    ### 4. Durum Yönetimi (State Management) ve API Entegrasyonu
    * **API Entegrasyon Yaklaşımı:** <Mock servislerin gerçek API uç noktalarıyla değiştirilmesi planı (Uygulamaya uygun asenkron veri çekme ve yönetim stratejileri)>
    * **Global State & Auth:** <Kullanıcı oturumu ve global uygulama verilerinin yönetimi için önerilen yaklaşım>

    ### 5. Adım Adım Implementasyon Planı
    * **Aşama 1 - Frontend Kod Analizi:** RapidNative çıktısındaki dosya yapısını, Expo Router yönlendirmelerini ve ekranlardaki yerel durumları (useState vb.) incele.
    * **Aşama 2 - Veritabanı ve Sunucu Kurulumu:** DB şemalarını oluştur, temel API sunucusunu (Express, FastAPI vb. veya serverless fonksiyonlar) ayağa kaldır.
    * **Aşama 3 - AI Servis Entegrasyonu:** Core AI fonksiyonunu ve agent mantığını backend üzerinde kodla, test et.
    * **Aşama 4 - API Bağlantısı ve State Entegrasyonu:** Frontend mock veri katmanlarını gerçek API çağrılarıyla değiştir. Yüklenme (loading) ve hata (error) durumlarını bağla.
    * **Aşama 5 - Uçtan Uca Doğrulama:** Arayüzün tüm akışlarını gerçek veri ve backend ile test et, bug-fix süreçlerini tamamla.
    [ARCHITECT_HANDOFF_BRIEF_END]
  </output_contract>

  <input_context>
    [RAKİP RAPORLARI VE FIRSAT HARİTALARI]:
    {kolektif_raporlar}
  </input_context>

  <recency_reminder>
    KRİTİK: Rapora hiçbir kişisel yorum veya giriş cümlesi ekleme. Doğrudan "# Master Niche Handoff & Prompt Blueprint: {anahtar_kelime}" başlığıyla başla. Çıktı formatına, hiyerarşiye ve XML sınırlarına tam olarak sadık kal.
  </recency_reminder>
</system_instructions>"""

NICHE_SYNTHESIS_PROMPT: str = os.getenv("NICHE_SYNTHESIS_PROMPT", _DEFAULT_NICHE_SYNTHESIS_PROMPT)

# LLM Sağlayıcı Seçimi — varsayılan: openrouter
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openrouter").lower()

if LLM_PROVIDER not in _SUPPORTED_PROVIDERS:
    raise ValueError(
        f"Desteklenmeyen LLM_PROVIDER: '{LLM_PROVIDER}'. "
        f"Geçerli seçenekler: {', '.join(_SUPPORTED_PROVIDERS)}"
    )

if LLM_PROVIDER == "deepseek":
    DEEPSEEK_API_KEY: str = _get_required("DEEPSEEK_API_KEY")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
    LLM_MODEL, _thinking_default = _normalize_deepseek_model(DEEPSEEK_MODEL)
    LLM_THINKING_ENABLED: bool = _as_bool(
        os.getenv("DEEPSEEK_THINKING_ENABLED"),
        _thinking_default,
    )
    LLM_REASONING_EFFORT: str | None = _normalize_reasoning_effort(
        os.getenv("DEEPSEEK_REASONING_EFFORT"),
        "high" if LLM_THINKING_ENABLED else None,
    )
    LLM_EXTRA_BODY: dict[str, dict[str, str]] | None = (
        {"thinking": {"type": "enabled"}} if LLM_THINKING_ENABLED else None
    )
    LLM_API_KEY: str = DEEPSEEK_API_KEY
    LLM_BASE_URL: str = "https://api.deepseek.com"
else:  # openrouter
    OPENROUTER_API_KEY: str = _get_required("OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = _get_required("OPENROUTER_MODEL")
    LLM_API_KEY: str = OPENROUTER_API_KEY
    LLM_MODEL: str = OPENROUTER_MODEL
    LLM_BASE_URL: str = "https://openrouter.ai/api/v1"
    LLM_THINKING_ENABLED: bool = False
    LLM_REASONING_EFFORT: str | None = None
    LLM_EXTRA_BODY: dict[str, dict[str, str]] | None = None
