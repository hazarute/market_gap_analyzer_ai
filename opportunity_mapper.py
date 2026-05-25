import os
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from report_generator import _safe_filename


def build_opportunity_map(report_path: str) -> str:
    """Mevcut rapor dosyasını LangChain zinciriyle işleyerek fırsat haritası üretir.

    Args:
        report_path: Kaynak rapor dosyasının tam yolu.

    Returns:
        Fırsat haritası Markdown metni.

    Raises:
        FileNotFoundError: Kaynak rapor dosyası bulunamazsa.
        RuntimeError: LLM boş yanıt döndürürse.
    """
    report_file = Path(report_path)
    if not report_file.exists():
        raise FileNotFoundError(f"Kaynak rapor dosyası bulunamadı: {report_path}")

    report_content = report_file.read_text(encoding="utf-8")

    prompt_template = config.OPPORTUNITY_MAP_PROMPT
    prompt = PromptTemplate(
        input_variables=["rapor_icerigi"],
        template=prompt_template,
    )

    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        api_key=lambda: config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
        extra_body=config.LLM_EXTRA_BODY,
        reasoning_effort=config.LLM_REASONING_EFFORT,
    )

    chain = prompt | llm | StrOutputParser()
    result: str = chain.invoke({"rapor_icerigi": report_content})

    if not result or not result.strip():
        raise RuntimeError("LLM boş yanıt döndürdü; fırsat haritası üretilemedi.")

    return result


def map_opportunity(
    report_path: str,
    app_name: str,
    reports_dir: str = "reports",
) -> str:
    """Fırsat haritasını üretir ve dosyaya kaydeder.

    Args:
        report_path: Kaynak rapor dosyasının tam yolu.
        app_name: Uygulama adı (dosya adı için kullanılır).
        reports_dir: Çıktı klasörü (varsayılan: 'reports').

    Returns:
        Oluşturulan fırsat haritası dosyasının yolu.
    """
    opportunity_content = build_opportunity_map(report_path)

    safe_name = _safe_filename(app_name)
    app_dir = os.path.join(reports_dir, safe_name)
    output_path = os.path.join(app_dir, f"opportunity_map_{safe_name}.md")

    os.makedirs(app_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Fırsat Haritası: {app_name}\n\n")
        f.write(opportunity_content)

    return output_path
