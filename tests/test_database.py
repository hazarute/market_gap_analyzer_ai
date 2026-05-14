import sqlite3
import tempfile
import os

import pytest

import database


@pytest.fixture
def db_conn():
    """Her test için izole geçici veritabanı bağlantısı sağlar."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    conn = database.init_db(db_path)
    yield conn
    conn.close()
    os.unlink(db_path)


def test_init_db_creates_table(db_conn):
    """init_db() analiz_gecmisi tablosunu oluşturmalı."""
    cursor = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='analiz_gecmisi'"
    )
    assert cursor.fetchone() is not None


def test_init_db_includes_description_column(db_conn):
    """analiz_gecmisi tablosunda description sütunu olmalı."""
    cursor = db_conn.execute("PRAGMA table_info(analiz_gecmisi)")
    columns = [row[1] for row in cursor.fetchall()]
    assert "description" in columns


def test_is_analyzed_returns_false_for_new_app(db_conn):
    """Daha önce kaydedilmemiş app_id için False dönmeli."""
    assert database.is_analyzed(db_conn, "com.new.app") is False


def test_save_and_is_analyzed(db_conn):
    """Kaydedilen app_id için is_analyzed() True dönmeli."""
    database.save_analysis(db_conn, "com.test.app", "Test App", "android", "rapor_test.md")
    assert database.is_analyzed(db_conn, "com.test.app") is True


def test_save_analysis_insert_or_ignore(db_conn):
    """Aynı app_id iki kez kaydedilmeye çalışılırsa hata fırlatılmamalı."""
    database.save_analysis(db_conn, "com.dup.app", "Dup App", "android", "rapor_dup.md")
    database.save_analysis(db_conn, "com.dup.app", "Dup App", "android", "rapor_dup.md")
    cursor = db_conn.execute(
        "SELECT COUNT(*) FROM analiz_gecmisi WHERE app_id = ?", ("com.dup.app",)
    )
    assert cursor.fetchone()[0] == 1


def test_save_analysis_stores_correct_fields(db_conn):
    """Kaydedilen satır doğru alan değerlerini içermeli."""
    database.save_analysis(
        db_conn,
        "com.field.app",
        "Field App",
        "ios",
        "rapor_field.md",
        "Türkçe açıklama",
    )
    cursor = db_conn.execute(
        "SELECT app_name, store, report_path, description FROM analiz_gecmisi WHERE app_id = ?",
        ("com.field.app",),
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "Field App"
    assert row[1] == "ios"
    assert row[2] == "rapor_field.md"
    assert row[3] == "Türkçe açıklama"


def test_is_analyzed_different_apps_are_independent(db_conn):
    """Farklı app_id'ler birbirini etkilememeli."""
    database.save_analysis(db_conn, "com.app.one", "App One", "android", "rapor_one.md")
    assert database.is_analyzed(db_conn, "com.app.one") is True
    assert database.is_analyzed(db_conn, "com.app.two") is False


def test_init_db_includes_opportunity_map_columns(db_conn):
    """analiz_gecmisi tablosu opportunity_map_path ve opportunity_map_at sütunlarını içermeli."""
    cursor = db_conn.execute("PRAGMA table_info(analiz_gecmisi)")
    columns = [row[1] for row in cursor.fetchall()]
    assert "opportunity_map_path" in columns
    assert "opportunity_map_at" in columns


def test_init_db_includes_master_prompt_columns(db_conn):
    """analiz_gecmisi tablosu master_prompt_path ve master_prompt_at sütunlarını içermeli."""
    cursor = db_conn.execute("PRAGMA table_info(analiz_gecmisi)")
    columns = [row[1] for row in cursor.fetchall()]
    assert "master_prompt_path" in columns
    assert "master_prompt_at" in columns


def test_save_opportunity_map_updates_record(db_conn):
    """save_opportunity_map() mevcut kayda opportunity_map_path yazmalı."""
    database.save_analysis(db_conn, "com.opp.app", "Opp App", "android", "rapor_opp.md")
    database.save_opportunity_map(db_conn, "com.opp.app", "reports/opportunity_map_opp.md")

    cursor = db_conn.execute(
        "SELECT opportunity_map_path, opportunity_map_at FROM analiz_gecmisi WHERE app_id = ?",
        ("com.opp.app",),
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "reports/opportunity_map_opp.md"
    assert row[1] is not None


def test_save_master_prompt_updates_record(db_conn):
    """save_master_prompt() mevcut kayda master_prompt_path yazmalı."""
    database.save_analysis(db_conn, "com.mp.app", "MP App", "ios", "rapor_mp.md")
    database.save_master_prompt(db_conn, "com.mp.app", "reports/master_prompt_mp.md")

    cursor = db_conn.execute(
        "SELECT master_prompt_path, master_prompt_at FROM analiz_gecmisi WHERE app_id = ?",
        ("com.mp.app",),
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == "reports/master_prompt_mp.md"
    assert row[1] is not None


def test_save_opportunity_map_does_not_overwrite_base_analysis(db_conn):
    """save_opportunity_map() rapor_path veya app_name alanlarını değiştirmemeli."""
    database.save_analysis(db_conn, "com.intact.app", "Intact App", "android", "rapor_intact.md")
    database.save_opportunity_map(db_conn, "com.intact.app", "reports/opportunity_map_intact.md")

    cursor = db_conn.execute(
        "SELECT app_name, report_path FROM analiz_gecmisi WHERE app_id = ?",
        ("com.intact.app",),
    )
    row = cursor.fetchone()
    assert row[0] == "Intact App"
    assert row[1] == "rapor_intact.md"
