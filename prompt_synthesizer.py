import os
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from report_generator import _safe_filename


def synthesize_master_prompt(
    report_path: str,
    opportunity_map_path: str,
) -> str:
    """İki raporu LangChain zinciriyle sentezleyerek master prompt üretir.

    Args:
        report_path: Birinci aşama rapor dosyasının tam yolu.
        opportunity_map_path: İkinci aşama fırsat haritası dosyasının tam yolu.

    Returns:
        Master prompt Markdown metni.

    Raises:
        FileNotFoundError: Kaynak dosyalardan biri bulunamazsa.
        RuntimeError: LLM boş yanıt döndürürse.
    """
    for path in (report_path, opportunity_map_path):
        if not Path(path).exists():
            raise FileNotFoundError(f"Kaynak dosya bulunamadı: {path}")

    report_content = Path(report_path).read_text(encoding="utf-8")
    opportunity_content = Path(opportunity_map_path).read_text(encoding="utf-8")

    prompt_template = config.SYNTHESIS_PROMPT
    prompt = PromptTemplate(
        input_variables=["rapor_icerigi", "firsat_haritasi_icerigi"],
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
    result: str = chain.invoke(
        {
            "rapor_icerigi": report_content,
            "firsat_haritasi_icerigi": opportunity_content,
        }
    )

    if not result or not result.strip():
        raise RuntimeError("LLM boş yanıt döndürdü; master prompt üretilemedi.")

    return result


def create_master_prompt(
    report_path: str,
    opportunity_map_path: str,
    app_name: str,
    reports_dir: str = "reports",
) -> str:
    """Master promptu üretir ve dosyaya kaydeder.

    Args:
        report_path: Birinci aşama rapor dosyasının tam yolu.
        opportunity_map_path: İkinci aşama fırsat haritası dosyasının tam yolu.
        app_name: Uygulama adı (dosya adı için kullanılır).
        reports_dir: Çıktı klasörü (varsayılan: 'reports').

    Returns:
        Oluşturulan master prompt dosyasının yolu.
    """
    master_content = synthesize_master_prompt(report_path, opportunity_map_path)

    safe_name = _safe_filename(app_name)
    app_dir = os.path.join(reports_dir, safe_name)
    output_path = os.path.join(app_dir, f"master_prompt_{safe_name}.md")

    os.makedirs(app_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Master LLM Prompt: {app_name}\n\n")
        f.write(
            "> Bu belge frontier modellere (Claude Opus, Gemini Pro, GPT-5) "
            "doğrudan yapıştırılmak üzere otomatik sentezlenmiştir.\n\n"
        )
        f.write("---\n\n")
        f.write(master_content)

    return output_path


def synthesize_niche_prompt(
    keyword: str,
    reports_and_opportunities: list[dict],
) -> str:
    """Birden fazla uygulamanın analiz ve fırsat raporlarını sentezleyerek tek bir niş master prompt üretir.

    Args:
        keyword: Arama kelimesi.
        reports_and_opportunities: Her biri {"app_name": str, "report_path": str, "opportunity_map_path": str} içeren liste.

    Returns:
        Sentezlenmiş niş master prompt metni.
    """
    if not reports_and_opportunities:
        raise ValueError("Sentezlenecek rapor bulunamadı.")

    collective_content = []
    for idx, item in enumerate(reports_and_opportunities, 1):
        app_name = item["app_name"]
        rep_path = item.get("report_path")
        opp_path = item.get("opportunity_map_path")

        app_text = f"### RAKİP {idx}: {app_name}\n"

        if rep_path and Path(rep_path).exists():
            rep_text = Path(rep_path).read_text(encoding="utf-8")
            app_text += f"#### Pazar Analiz Raporu:\n{rep_text}\n\n"

        if opp_path and Path(opp_path).exists():
            opp_text = Path(opp_path).read_text(encoding="utf-8")
            app_text += f"#### Fırsat Haritası:\n{opp_text}\n\n"

        collective_content.append(app_text)

    kolektif_raporlar = "\n\n---\n\n".join(collective_content)

    prompt_template = config.NICHE_SYNTHESIS_PROMPT
    prompt = PromptTemplate(
        input_variables=["anahtar_kelime", "kolektif_raporlar"],
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
    result: str = chain.invoke(
        {
            "anahtar_kelime": keyword,
            "kolektif_raporlar": kolektif_raporlar,
        }
    )

    if not result or not result.strip():
        raise RuntimeError("LLM boş yanıt döndürdü; niş master prompt üretilemedi.")

    return result


def create_niche_prompt(
    keyword: str,
    reports_and_opportunities: list[dict],
    reports_dir: str = "reports",
) -> str:
    """Niş sentezlenmiş promptu üretir ve dosyaya kaydeder.

    Args:
        keyword: Arama kelimesi.
        reports_and_opportunities: Rapor ve fırsat haritası yollarını içeren liste.
        reports_dir: Çıktı klasörü.

    Returns:
        Oluşturulan dosyanın yolu.
    """
    niche_content = synthesize_niche_prompt(keyword, reports_and_opportunities)

    safe_keyword = _safe_filename(keyword)
    output_dir = os.path.join(reports_dir, f"niche_{safe_keyword}")
    output_path = os.path.join(output_dir, f"niche_master_prompt_{safe_keyword}.md")

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Master Niche Handoff & Prompt Blueprint: {keyword}\n\n")
        f.write(
            "> Bu belge, belirli bir anahtar kelime altındaki tüm rakiplerin pazar boşlukları "
            "ve fırsat analizleri ortak sentezlenerek, frontier modellere "
            "(Claude Opus, Gemini Pro, GPT-5) doğrudan yapıştırılmak üzere otomatik üretilmiştir.\n\n"
        )
        f.write("---\n\n")
        f.write(niche_content)

    return output_path

