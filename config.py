import os

from dotenv import load_dotenv

load_dotenv()

_REQUIRED_VARS = (
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
    "ANALYSIS_PROMPT",
)


def _get_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"Zorunlu ortam değişkeni eksik: '{name}'. "
            f".env dosyanızı kontrol edin (şablon: .env.example)."
        )
    return value


OPENROUTER_API_KEY: str = _get_required("OPENROUTER_API_KEY")
OPENROUTER_MODEL: str = _get_required("OPENROUTER_MODEL")
ANALYSIS_PROMPT: str = _get_required("ANALYSIS_PROMPT")
DATABASE_PATH: str = os.getenv("DATABASE_PATH", "analiz_gecmisi.db")

# Opsiyonel: tanımlanmazsa ilgili modüldeki varsayılan şablon devreye girer.
OPPORTUNITY_MAP_PROMPT: str | None = os.getenv("OPPORTUNITY_MAP_PROMPT") or None
SYNTHESIS_PROMPT: str | None = os.getenv("SYNTHESIS_PROMPT") or None
