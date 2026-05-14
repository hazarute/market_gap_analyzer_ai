import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

import opportunity_mapper


@pytest.fixture
def sample_report_file(tmp_path):
    """Geçici bir örnek rapor dosyası oluşturur."""
    report = tmp_path / "rapor_test_app.md"
    report.write_text("# Pazar Analizi\n\n## Market Gap\nKullanıcılar otomasyon istiyor.\n", encoding="utf-8")
    return str(report)


@patch("opportunity_mapper.ChatOpenAI")
@patch("opportunity_mapper.StrOutputParser")
@patch("opportunity_mapper.PromptTemplate")
def test_build_opportunity_map_returns_string(mock_template_cls, mock_parser_cls, mock_llm_cls, sample_report_file):
    """build_opportunity_map() LLM çıktısını string olarak döndürmeli."""
    mock_chain_result = "## Öncelikli Fırsat Alanları\n1. Otomasyon boşluğu\n"

    # prompt | llm → mid_chain; mid_chain | parser → final_chain
    final_chain = MagicMock()
    final_chain.invoke.return_value = mock_chain_result

    mid_chain = MagicMock()
    mid_chain.__or__ = MagicMock(return_value=final_chain)

    mock_prompt = MagicMock()
    mock_prompt.__or__ = MagicMock(return_value=mid_chain)
    mock_template_cls.return_value = mock_prompt

    result = opportunity_mapper.build_opportunity_map(sample_report_file)

    assert isinstance(result, str)
    assert result == mock_chain_result


def test_build_opportunity_map_raises_if_file_missing():
    """Kaynak rapor yoksa FileNotFoundError fırlatılmalı."""
    with pytest.raises(FileNotFoundError):
        opportunity_mapper.build_opportunity_map("/tmp/var_olmayan_dosya.md")


@patch("opportunity_mapper.build_opportunity_map")
def test_map_opportunity_creates_file(mock_build, tmp_path, sample_report_file):
    """map_opportunity() opportunity_map_*.md dosyasını oluşturmalı."""
    mock_build.return_value = "## Fırsat 1\nOtomasyon boşluğu mevcut."
    reports_dir = str(tmp_path / "reports")

    output_path = opportunity_mapper.map_opportunity(
        sample_report_file, "Test App", reports_dir=reports_dir
    )

    assert os.path.isfile(output_path)
    assert "opportunity_map_" in os.path.basename(output_path)
    assert output_path.endswith(".md")


@patch("opportunity_mapper.build_opportunity_map")
def test_map_opportunity_file_contains_app_name(mock_build, tmp_path, sample_report_file):
    """Oluşturulan dosya uygulama adını başlıkta içermeli."""
    mock_build.return_value = "Fırsat içeriği"
    reports_dir = str(tmp_path / "reports")

    output_path = opportunity_mapper.map_opportunity(
        sample_report_file, "Monefy", reports_dir=reports_dir
    )

    content = open(output_path, encoding="utf-8").read()
    assert "Monefy" in content


@patch("opportunity_mapper.build_opportunity_map")
def test_map_opportunity_file_contains_llm_output(mock_build, tmp_path, sample_report_file):
    """Dosya LLM çıktısını içermeli."""
    llm_output = "## Rekabet Kör Noktaları\nMobil otomasyon yok."
    mock_build.return_value = llm_output
    reports_dir = str(tmp_path / "reports")

    output_path = opportunity_mapper.map_opportunity(
        sample_report_file, "TestApp", reports_dir=reports_dir
    )

    content = open(output_path, encoding="utf-8").read()
    assert llm_output in content


@patch("opportunity_mapper.build_opportunity_map")
def test_map_opportunity_safe_filename_special_chars(mock_build, tmp_path, sample_report_file):
    """Özel karakterler içeren uygulama adı güvenli dosya adına dönüştürülmeli."""
    mock_build.return_value = "İçerik"
    reports_dir = str(tmp_path / "reports")

    output_path = opportunity_mapper.map_opportunity(
        sample_report_file, "App! 2.0 #Beta", reports_dir=reports_dir
    )

    basename = os.path.basename(output_path)
    assert "!" not in basename
    assert "#" not in basename
    assert basename.endswith(".md")
