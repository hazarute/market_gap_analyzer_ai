from typing import Any

from openai import OpenAI

import config

_client = OpenAI(
    base_url=config.LLM_BASE_URL,
    api_key=config.LLM_API_KEY,
)

_MAX_REVIEW_CHARS = 3000
_MAX_DESC_CHARS = 2000


def _build_user_prompt(app_data: dict[str, Any]) -> str:
    """Uygulama verisinden LLM'e gönderilecek kullanıcı mesajını oluşturur."""
    app_name: str = app_data.get("app_name", "Bilinmiyor")
    store: str = app_data.get("store", "")
    score: float = app_data.get("score", 0.0)
    description: str = (app_data.get("description") or "")[:_MAX_DESC_CHARS]
    developer: str = app_data.get("developer", "")
    rating_count: int = app_data.get("rating_count", 0)

    reviews: list[str] = app_data.get("reviews") or []
    reviews_text = "\n".join(f"- {r}" for r in reviews if r)
    if len(reviews_text) > _MAX_REVIEW_CHARS:
        reviews_text = reviews_text[:_MAX_REVIEW_CHARS] + "\n..."

    store_label = "Google Play" if store == "android" else "Apple App Store"

    return (
        f"Uygulama Adı: {app_name}\n"
        f"Mağaza: {store_label}\n"
        f"Geliştirici: {developer}\n"
        f"Puan: {score:.1f} ({rating_count} değerlendirme)\n\n"
        f"Açıklama:\n{description}\n\n"
        f"Kullanıcı Yorumları (örnekler):\n{reviews_text if reviews_text else 'Yorum bulunamadı.'}"
    )


def _translate_description_to_turkish(description: str) -> str:
    """Açıklamayı Türkçeye çevirir; zaten Türkçe ise aynı metni döndürür."""
    if not description:
        return description

    prompt = (
        "Aşağıdaki metni Türkçeye çevir. Eğer metin zaten Türkçeyse, değişiklik yapma ve yalnızca çeviri metnini geri döndür."
        f"\n\n{description}"
    )

    response = _client.chat.completions.create(
        model=config.LLM_MODEL,
        extra_body=config.LLM_EXTRA_BODY,
        reasoning_effort=config.LLM_REASONING_EFFORT,
        messages=[
            {"role": "system", "content": "Sen deneyimli bir çeviri uzmanısın."},
            {"role": "user", "content": prompt},
        ],
    )

    translated = response.choices[0].message.content or ""
    return translated.strip() or description


def analyze_app(app_data: dict[str, Any]) -> str:
    """Uygulama verisini OpenRouter LLM ile analiz eder.

    Args:
        app_data: Scraper katmanından gelen standart uygulama sözlüğü.

    Returns:
        LLM'in ürettiği ham analiz metni.

    Raises:
        Exception: OpenRouter API çağrısı başarısız olursa yeniden fırlatılır;
                   main.py seviyesinde yakalanarak pipeline devam eder.
    """
    description = app_data.get("description")
    if isinstance(description, str) and description:
        app_data["description"] = _translate_description_to_turkish(description)

    user_prompt = _build_user_prompt(app_data)

    response = _client.chat.completions.create(
        model=config.LLM_MODEL,
        extra_body=config.LLM_EXTRA_BODY,
        reasoning_effort=config.LLM_REASONING_EFFORT,
        messages=[
            {"role": "system", "content": config.ANALYSIS_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content or ""
