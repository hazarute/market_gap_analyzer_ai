import os
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from report_generator import _safe_filename

_DEFAULT_OPPORTUNITY_MAP_PROMPT = """\
Sen kıdemli bir SaaS Growth Stratejisti ve Fırsat Analistisisin.

Aşağıda bir rakip uygulamanın pazar analiz raporu verilmiştir.
Bu raporu okuyarak yalnızca gerçekten boş olan ve yeni bir SaaS ile \
doldurulabilecek fırsat alanlarını haritalandır.

Üret:
1. Öncelikli Fırsat Alanları (3-5 madde, kanıta dayalı)
2. Hedef Müşteri Segmenti (en az 2 spesifik segment)
3. Rekabet Kör Noktaları (mevcut oyuncuların görmezden geldiği)
4. Hızlı Kazanım (0-3 ay içinde konumlandırılabilecek fırsat)
5. Orta Vadeli Fırsat (3-12 ay)
6. Uzun Vadeli Stratejik Pozisyon (12+ ay)
7. Risk Faktörleri (bu fırsatı zorlaştırabilecek 2-3 etken)

Rapor:
{rapor_icerigi}"""


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

    prompt_template = config.OPPORTUNITY_MAP_PROMPT or _DEFAULT_OPPORTUNITY_MAP_PROMPT
    prompt = PromptTemplate(
        input_variables=["rapor_icerigi"],
        template=prompt_template,
    )

    llm = ChatOpenAI(
        model=config.OPENROUTER_MODEL,
        api_key=config.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
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
