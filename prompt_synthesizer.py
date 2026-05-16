import os
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from report_generator import _safe_filename

_DEFAULT_SYNTHESIS_PROMPT = """\
Sen bir AI Ürün Stratejisti ve Prompt Mimarısısın.

Görev: Aşağıda iki kaynak belge verilmiştir:
  - [RAPOR]: Bir rakip uygulamanın derinlemesine pazar analizi
  - [FIRSAT HARİTASI]: Bu analizden çıkarılan fırsat alanları

Bu iki belgeyi sentezleyerek, Claude Opus / Gemini Pro / GPT-5 seviyesinde \
bir frontier AI modeline verilmek üzere "tek seferde çalışan" kapsamlı bir \
master prompt üret.

Master prompt aşağıdaki bölümleri içermelidir:
1. Görev Çerçevesi (frontier modelin ne yapması gerektiği)
2. Bağlam Paketi (pazar özeti, fırsat alanları, rekabet kör noktaları)
3. Kısıtlar ve Varsayımlar (bütçe, timeline, minimum ekip büyüklüğü)
4. İstenen Çıktı Formatı (MVP planı, GTM stratejisi veya yatırımcı sunumu)
5. Kalite Eşiği (kabul edilebilir minimum çıktı standartları)
6. Örnek Giriş / Beklenen Çıktı Formatı

[RAPOR]:
{rapor_icerigi}

[FIRSAT HARİTASI]:
{firsat_haritasi_icerigi}"""


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

    prompt_template = config.SYNTHESIS_PROMPT or _DEFAULT_SYNTHESIS_PROMPT
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
