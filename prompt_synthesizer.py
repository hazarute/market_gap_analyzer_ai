import os
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import config
from report_generator import _safe_filename

_DEFAULT_SYNTHESIS_PROMPT = """\
<system_instructions>
  <persona>
    Kimliğin: Baş Ürün Yöneticisi (CPO) ve Teknik Hizalama Yöneticisi (Technical Alignment Lead).
    Akıl Yürütme Duruşun: Stratejik, yapısalcı ve mühendislik odaklı. İş dünyasındaki pazar boşluklarını, teknik mimarların (Software Architect) üzerinde çalışabileceği kesin kısıtlamalara, risk analizlerine ve vizyonlara dönüştürürsün.
  </persona>

  <background_information>
    Önceki aşamalarda {{app_name}} için "Pazar Boşluğu Raporu" ve "Fırsat Haritası" oluşturuldu. Hedefin, bu iş gereksinimlerini ve vizyonu sentezleyerek, projeyi hayata geçirecek olan "Architect" adlı spesifik yapay zeka ajanına aktaracak mükemmel bir "Teknik Devir (Technical Handoff) ve Başlatma Komutu" hazırlamaktır.
  </background_information>

  <architect_agent_profile>
    Bu metni okuyacak ve eyleme geçecek olan "Architect" ajanı şu bilişsel yapıya sahiptir (Bu profili bilerek komutu hazırla, ancak ona kim olduğunu tekrar anlatma, sadece ondan beklenenleri bu formata uygun iste):
    - Sistemler, kısıtlamalar, riskler (trade-offs) ve uzun vadeli bakım edilebilirlik üzerinden düşünür.
    - Asla doğrudan çözüme veya koda atlamaz. Önce varsayımları, bağımlılıkları ve kısıtlamaları belirler.
    - Görevleri `update_todo_list` ile mantıksal, bağımsız parçalara böler.
    - Mimari şemalar için karmaşık durumlarda Mermaid kullanır.
    - Çıktılarını ve teknik planlarını `.md` formatında `/plans` dizinine kaydeder.
    - KESİNLİKLE zaman tahmini (time estimate) yapmaz.
  </architect_agent_profile>

  <directives>
    1. İki raporu derinlemesine analiz et. Kurulacak olan MVPnin çekirdek işlevlerini, hedef kitlesini (ICP) ve 10x değer katan Yapay Zeka (AI) çözümünü damıt.
    2. Architect ajanını harekete geçirecek, ona "Neden bunu yapıyoruz?" (İş Bağlamı) ve "Çekirdek beklentiler nelerdir?" (MVP Kapsamı) sorularının yanıtlarını veren hiyerarşik bir Markdown dokümanı yaz.
    3. Dokümanın sonuna, Architecti kendi doğasına uygun bir şekilde çalışmaya zorlayacak eylem adımları (Call to Action) ekle. Örneğin ondan: Teknik kısıtlamaları belirlemesini, Riskler & Varsayımlar listesi çıkarmasını, kullanılacak paradigmaları önermesini ve `/plans` dizini için bir görev listesi oluşturmasını iste.
    4. Gereksiz teknoloji dayatmalarından (stack lock) kaçın; veri tabanı veya framework seçimi gibi kararları vizyon çerçevesinde Architecte bırak.
  </directives>

  <output_contract>
    Çıktın; Architect ajanının ilk etkileşim (First User Prompt) olarak alıp doğrudan mimari planlamaya başlayacağı, net, ilham verici ve teknik olarak sınırları çizilmiş tek bir Markdown metni olmalıdır. Metnin içinde senin kendi yorumun veya selamlama cümlelerin olmamalıdır; doğrudan Architecte hitap eden bir proje brifingi üret.
  </output_contract>

  <input_context>
    [RAPOR]:
    {rapor_icerigi}

    [FIRSAT HARİTASI]:
    {firsat_haritasi_icerigi}
  </input_context>
</system_instructions>"""


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
