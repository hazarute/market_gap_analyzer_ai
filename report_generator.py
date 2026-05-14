import re
from datetime import datetime, timezone
from pathlib import Path


def _safe_filename(app_name: str) -> str:
    """Uygulama adından güvenli bir dosya adı parçası üretir."""
    name = app_name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "_", name)
    return name[:60]


def _summarize_description(description: str, max_length: int = 180) -> str:
    """Uzun uygulama açıklamasını kısa, tek satırlık bir özet halinde döndürür."""
    text = " ".join(description.strip().split())
    if len(text) <= max_length:
        return text

    sentences = re.split(r"(?<=[.!?])\s+", text)
    if sentences:
        first_sentence = sentences[0].strip()
        if len(first_sentence) <= max_length:
            return first_sentence + ("..." if len(text) > len(first_sentence) else "")

    return text[:max_length].rstrip(" \t.,;:!?") + "..."


def generate_report(app_name: str, analysis_result: str, app_data: dict[str, str] | None = None) -> str:
    """Analiz sonucunu Markdown dosyası olarak kaydeder.

    Args:
        app_name: Uygulamanın adı (dosya adı oluşturmak için kullanılır).
        analysis_result: analyzer.analyze_app() tarafından döndürülen ham metin.
        app_data: Opsiyonel uygulama meta verisi.

    Returns:
        Kaydedilen dosyanın yolu (str).
    """
    safe_name = _safe_filename(app_name)
    filename = f"rapor_{safe_name}.md"
    output_dir = Path("reports") / safe_name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    metadata_section = ""
    if app_data:
        store_label = "Google Play" if app_data.get("store") == "android" else "Apple App Store"
        metadata_lines = [
            f"- **Uygulama Adı:** {app_name}",
            f"- **Mağaza:** {store_label}",
        ]
        app_id = app_data.get("app_id")
        if app_id:
            metadata_lines.append(f"- **App ID:** {app_id}")
        developer = app_data.get("developer")
        if developer:
            metadata_lines.append(f"- **Geliştirici:** {developer}")
        score = app_data.get("score")
        if score is not None:
            metadata_lines.append(f"- **Puan:** {score}")
        rating_count = app_data.get("rating_count")
        if rating_count is not None:
            metadata_lines.append(f"- **Değerlendirme Sayısı:** {rating_count}")
        description = app_data.get("description")
        if description:
            short_description = _summarize_description(description)
            metadata_lines.append(f"- **Açıklama:** {short_description}")

        metadata_section = (
            "## Uygulama Bilgileri\n\n"
            + "\n".join(metadata_lines)
            + "\n\n---\n\n"
        )

    content = (
        f"# Pazar Analizi: {app_name}\n\n"
        f"> Oluşturulma: {timestamp}\n\n"
        f"---\n\n"
        f"{metadata_section}"
        f"{analysis_result}\n"
    )

    output_path.write_text(content, encoding="utf-8")
    return str(output_path)
