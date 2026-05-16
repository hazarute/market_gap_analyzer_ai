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

# Opsiyonel: tanımlanmazsa ilgili modüldeki varsayılan şablon devreye girer.
OPPORTUNITY_MAP_PROMPT: str | None = os.getenv("OPPORTUNITY_MAP_PROMPT") or None
SYNTHESIS_PROMPT: str | None = os.getenv("SYNTHESIS_PROMPT") or None

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
