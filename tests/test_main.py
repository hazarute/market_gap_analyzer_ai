import importlib
import sys

import pytest


@pytest.fixture
def main_module(monkeypatch):
    monkeypatch.setenv("ANALYSIS_PROMPT", "prompt")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test-openrouter-model")
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")

    sys.modules.pop("config", None)
    sys.modules.pop("main", None)
    return importlib.import_module("main")


def test_parse_args_accepts_multiple_stores(main_module, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["main.py", "--keyword", "test", "--store", "android", "ios"],
    )

    args = main_module.parse_args()

    assert args.keyword == "test"
    assert args.store == ["android", "ios"]


def test_run_processes_android_and_ios(main_module, monkeypatch):
    calls = {
        "gp_search": [],
        "as_search": [],
        "gp_details": [],
        "as_details": [],
        "save_analysis": [],
        "reports": [],
        "closed": False,
    }

    class DummyConn:
        def close(self):
            calls["closed"] = True

    def fake_gp_search(keyword, n_hits, offset=0):
        calls["gp_search"].append((keyword, n_hits, offset))
        return [{"app_id": "android-1", "app_name": "Android App"}]

    def fake_as_search(keyword, n_hits, offset=0):
        calls["as_search"].append((keyword, n_hits, offset))
        return [{"app_id": "ios-1", "app_name": "iOS App"}]

    def fake_gp_details(app_id):
        calls["gp_details"].append(app_id)
        return {"app_id": app_id, "store": "android", "description": "Android desc"}

    def fake_as_details(app_id):
        calls["as_details"].append(app_id)
        return {"app_id": app_id, "store": "ios", "description": "iOS desc"}

    def fake_generate_report(app_name, analysis_result, detailed, store=""):
        calls["reports"].append((app_name, analysis_result, detailed["app_id"]))
        return f"reports/{app_name}.md"

    def fake_save_analysis(conn, app_id, app_name, store, report_path, description=None):
        calls["save_analysis"].append((app_id, app_name, store, report_path, description))

    monkeypatch.setattr(main_module.config, "DATABASE_PATH", "test.db")
    monkeypatch.setattr(main_module.database, "init_db", lambda _path: DummyConn())
    monkeypatch.setattr(main_module.database, "is_analyzed", lambda _conn, _app_id: False)
    monkeypatch.setattr(main_module.database, "save_analysis", fake_save_analysis)
    monkeypatch.setattr(main_module.database, "save_opportunity_map", lambda *args, **kwargs: None)
    monkeypatch.setattr(main_module.database, "save_master_prompt", lambda *args, **kwargs: None)
    monkeypatch.setattr(main_module, "gp_search", fake_gp_search)
    monkeypatch.setattr(main_module, "as_search", fake_as_search)
    monkeypatch.setattr(main_module, "gp_details", fake_gp_details)
    monkeypatch.setattr(main_module, "as_details", fake_as_details)
    monkeypatch.setattr(main_module, "generate_report", fake_generate_report)
    monkeypatch.setattr(main_module, "analyze_app", lambda detailed: f"analysis:{detailed['app_id']}")

    main_module.run(keyword="test", stores=["android", "ios"], limit=1)

    assert calls["gp_search"] == [("test", 1, 0)]
    assert calls["as_search"] == [("test", 1, 0)]
    assert calls["gp_details"] == ["android-1"]
    assert calls["as_details"] == ["ios-1"]
    assert [entry[2] for entry in calls["save_analysis"]] == ["android", "ios"]
    assert calls["closed"] is True


def test_run_auto_paginates_skipped_apps(main_module, monkeypatch):
    """Analiz edilmiş uygulamalar atlanarak bir sonraki batch'e otomatik geçilmeli."""
    search_calls = []
    analyzed_ids = {"android-old-1"}
    details_calls = []
    save_calls = []

    class DummyConn:
        def close(self):
            pass

    def fake_gp_search(keyword, n_hits, offset=0):
        search_calls.append(offset)
        if offset == 0:
            return [{"app_id": "android-old-1", "app_name": "Old App"}]
        return [{"app_id": "android-new-1", "app_name": "New App"}]

    def fake_is_analyzed(conn, app_id):
        return app_id in analyzed_ids

    def fake_gp_details(app_id):
        details_calls.append(app_id)
        return {"app_id": app_id, "store": "android", "description": "desc"}

    def fake_generate_report(app_name, analysis_result, detailed, store=""):
        return f"reports/{app_name}.md"

    def fake_save_analysis(conn, app_id, app_name, store, report_path, description=None):
        save_calls.append(app_id)

    monkeypatch.setattr(main_module.config, "DATABASE_PATH", "test.db")
    monkeypatch.setattr(main_module.database, "init_db", lambda _path: DummyConn())
    monkeypatch.setattr(main_module.database, "is_analyzed", fake_is_analyzed)
    monkeypatch.setattr(main_module.database, "save_analysis", fake_save_analysis)
    monkeypatch.setattr(main_module.database, "save_opportunity_map", lambda *args, **kwargs: None)
    monkeypatch.setattr(main_module.database, "save_master_prompt", lambda *args, **kwargs: None)
    monkeypatch.setattr(main_module, "gp_search", fake_gp_search)
    monkeypatch.setattr(main_module, "gp_details", fake_gp_details)
    monkeypatch.setattr(main_module, "generate_report", fake_generate_report)
    monkeypatch.setattr(main_module, "analyze_app", lambda detailed: "analysis")

    main_module.run(keyword="test", stores=["android"], limit=1)

    # İlk batch atlandı (zaten analiz edilmiş), ikinci batch'e geçilmeli
    assert 0 in search_calls, "İlk offset=0 çağrısı yapılmalı"
    assert 1 in search_calls, "Otomatik ilerleme için offset=1 çağrısı yapılmalı"
    # Yeni uygulama analiz edilmeli, eski uygulama analiz edilmemeli
    assert details_calls == ["android-new-1"]
    assert save_calls == ["android-new-1"]