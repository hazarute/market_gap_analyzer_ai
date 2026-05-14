import os
import tempfile

import pytest

import report_generator


@pytest.fixture(autouse=True)
def isolated_tmp_dir(monkeypatch, tmp_path):
    """Her test dosya çıktısını geçici dizine yönlendirir."""
    monkeypatch.chdir(tmp_path)


def test_generate_report_creates_file():
    """generate_report() bir dosya oluşturmalı ve yolunu döndürmeli."""
    path = report_generator.generate_report("Test App", "Analiz sonucu buraya gelir.")
    assert os.path.isfile(path)
    # Yeni yapı: reports/{safe_name}/rapor_{safe_name}.md
    parts = os.path.normpath(path).split(os.sep)
    assert "reports" in parts
    app_dir = os.path.basename(os.path.dirname(path))
    assert app_dir == "test_app"


def test_generate_report_filename_format():
    """Dosya adı 'rapor_' önekiyle başlamalı ve .md uzantısı içermeli."""
    path = report_generator.generate_report("Spotify", "İçerik")
    assert os.path.basename(path).startswith("rapor_")
    assert path.endswith(".md")


def test_generate_report_content_includes_app_name():
    """Rapor içeriği uygulama adını başlıkta içermeli."""
    path = report_generator.generate_report("Monefy", "Pain point analizi.")
    content = open(path, encoding="utf-8").read()
    assert "Monefy" in content


def test_generate_report_content_includes_analysis():
    """Rapor içeriği analiz metnini içermeli."""
    analysis = "## Market Gap\nKullanıcılar otomasyondan yoksun."
    path = report_generator.generate_report("TestApp", analysis)
    content = open(path, encoding="utf-8").read()
    assert analysis in content


def test_generate_report_safe_filename_special_chars():
    """Özel karakter içeren uygulama adı güvenli dosya adına dönüştürülmeli."""
    path = report_generator.generate_report("My App! 2.0 #Beta", "İçerik")
    basename = os.path.basename(path)
    assert "!" not in basename
    assert "#" not in basename
    assert basename.endswith(".md")


def test_generate_report_empty_analysis():
    """Boş analiz metniyle bile dosya oluşturulabilmeli."""
    path = report_generator.generate_report("EmptyApp", "")
    assert os.path.isfile(path)


def test_generate_report_includes_app_metadata():
    """Rapor, uygulama meta verilerini içermeli."""
    app_data = {
        "app_id": "12345",
        "store": "ios",
        "developer": "Test Developer",
        "score": 4.5,
        "rating_count": 250,
        "description": "Test açıklaması.",
    }
    path = report_generator.generate_report("Test App", "Analiz metni.", app_data)
    content = open(path, encoding="utf-8").read()
    assert "Uygulama Bilgileri" in content
    assert "Test Developer" in content
    assert "4.5" in content
    assert "Test açıklaması." in content


def test_generate_report_summarizes_long_description():
    """Uzun açıklama metni özetlenmeli."""
    long_description = (
        "Bu ürün birçok şekilde faydalıdır. "
        "Hemen hemen her türlü notu destekler, PDF, ses kaydı, görüntü, "
        "metin ve daha fazlasını saklar. Kullanıcılar projelerini organize edebilir, "
        "görev oluşturabilir ve farklı cihazlarda eşzamanlı çalışabilir. "
        "Ayrıca gelişmiş yapay zeka özellikleriyle içerik önerileri sunar."
    )
    app_data = {
        "app_id": "12345",
        "store": "ios",
        "developer": "Test Developer",
        "score": 4.5,
        "rating_count": 250,
        "description": long_description,
    }
    path = report_generator.generate_report("Test App", "Analiz metni.", app_data)
    content = open(path, encoding="utf-8").read()
    assert "Test Developer" in content
    assert "Açıklama:" in content
    assert len(content.split("Açıklama:")[1].split("\n")[0]) < len(long_description)
    assert "..." in content.split("Açıklama:")[1].split("\n")[0]
