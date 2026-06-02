import os
from unittest.mock import MagicMock, patch

import pytest

import prompt_synthesizer


@pytest.fixture
def sample_files(tmp_path):
    """Geçici rapor ve fırsat haritası dosyaları oluşturur."""
    report = tmp_path / "rapor_test.md"
    report.write_text("# Pazar Analizi\nPain point: otomasyon eksik.\n", encoding="utf-8")
    opp_map = tmp_path / "opportunity_map_test.md"
    opp_map.write_text("# Fırsat Haritası\n1. Hızlı kazanım: mobil otomasyon.\n", encoding="utf-8")
    return str(report), str(opp_map)


def test_synthesize_raises_if_report_missing(sample_files):
    """Rapor dosyası yoksa FileNotFoundError fırlatılmalı."""
    _, opp_map = sample_files
    with pytest.raises(FileNotFoundError):
        prompt_synthesizer.synthesize_master_prompt("/tmp/yok.md", opp_map)


def test_synthesize_raises_if_opportunity_map_missing(sample_files):
    """Fırsat haritası dosyası yoksa FileNotFoundError fırlatılmalı."""
    report, _ = sample_files
    with pytest.raises(FileNotFoundError):
        prompt_synthesizer.synthesize_master_prompt(report, "/tmp/yok.md")


@patch("prompt_synthesizer.synthesize_master_prompt")
def test_create_master_prompt_creates_file(mock_synthesize, tmp_path, sample_files):
    """create_master_prompt() master_prompt_*.md dosyasını oluşturmalı."""
    mock_synthesize.return_value = "## Görev Çerçevesi\nFrontier modele veril."
    report, opp_map = sample_files
    reports_dir = str(tmp_path / "reports")

    output_path = prompt_synthesizer.create_master_prompt(
        report, opp_map, "Evernote", reports_dir=reports_dir
    )

    assert os.path.isfile(output_path)
    assert "master_prompt_" in os.path.basename(output_path)
    assert output_path.endswith(".md")


@patch("prompt_synthesizer.synthesize_master_prompt")
def test_create_master_prompt_contains_app_name(mock_synthesize, tmp_path, sample_files):
    """Oluşturulan dosya uygulama adını başlıkta içermeli."""
    mock_synthesize.return_value = "Master prompt içeriği"
    report, opp_map = sample_files
    reports_dir = str(tmp_path / "reports")

    output_path = prompt_synthesizer.create_master_prompt(
        report, opp_map, "Notion", reports_dir=reports_dir
    )

    content = open(output_path, encoding="utf-8").read()
    assert "Notion" in content


@patch("prompt_synthesizer.synthesize_master_prompt")
def test_create_master_prompt_contains_frontier_disclaimer(mock_synthesize, tmp_path, sample_files):
    """Dosya frontier model uyarısını içermeli."""
    mock_synthesize.return_value = "İçerik"
    report, opp_map = sample_files
    reports_dir = str(tmp_path / "reports")

    output_path = prompt_synthesizer.create_master_prompt(
        report, opp_map, "TestApp", reports_dir=reports_dir
    )

    content = open(output_path, encoding="utf-8").read()
    assert "frontier" in content.lower() or "Claude" in content or "Gemini" in content


@patch("prompt_synthesizer.synthesize_master_prompt")
def test_create_master_prompt_contains_llm_output(mock_synthesize, tmp_path, sample_files):
    """Dosya LLM sentez çıktısını içermeli."""
    llm_output = "## Bağlam Paketi\nRakip zayıf noktaları: X, Y, Z."
    mock_synthesize.return_value = llm_output
    report, opp_map = sample_files
    reports_dir = str(tmp_path / "reports")

    output_path = prompt_synthesizer.create_master_prompt(
        report, opp_map, "TestApp", reports_dir=reports_dir
    )

    content = open(output_path, encoding="utf-8").read()
    assert llm_output in content


@patch("prompt_synthesizer.synthesize_master_prompt")
def test_create_master_prompt_safe_filename(mock_synthesize, tmp_path, sample_files):
    """Özel karakterler içeren uygulama adı güvenli dosya adına dönüştürülmeli."""
    mock_synthesize.return_value = "İçerik"
    report, opp_map = sample_files
    reports_dir = str(tmp_path / "reports")

    output_path = prompt_synthesizer.create_master_prompt(
        report, opp_map, "My App! #v2", reports_dir=reports_dir
    )

    basename = os.path.basename(output_path)
    assert "!" not in basename
    assert "#" not in basename
    assert basename.endswith(".md")


def test_synthesize_niche_prompt_raises_if_empty():
    """Boş rapor listesi gönderildiğinde ValueError fırlatılmalı."""
    with pytest.raises(ValueError):
        prompt_synthesizer.synthesize_niche_prompt("test", [])


@patch("prompt_synthesizer.synthesize_niche_prompt")
def test_create_niche_prompt_creates_file(mock_synthesize, tmp_path):
    """create_niche_prompt() dosyayı doğru şekilde oluşturmalı ve kaydetmeli."""
    mock_synthesize.return_value = "Sentezlenmiş niş içerik"
    reports_dir = str(tmp_path / "reports")

    reports_and_opportunities = [
        {"app_name": "App A", "report_path": "repA.md", "opportunity_map_path": "oppA.md"}
    ]

    output_path = prompt_synthesizer.create_niche_prompt(
        keyword="Proje Yönetimi",
        reports_and_opportunities=reports_and_opportunities,
        reports_dir=reports_dir,
    )

    assert os.path.isfile(output_path)
    assert "niche_master_prompt_" in os.path.basename(output_path)
    assert output_path.endswith(".md")

    content = open(output_path, encoding="utf-8").read()
    assert "Proje Yönetimi" in content
    assert "Sentezlenmiş niş içerik" in content

