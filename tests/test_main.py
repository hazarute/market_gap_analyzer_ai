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
        "gp_search": 0,
        "as_search": 0,
        "gp_details": [],
        "as_details": [],
        "save_analysis": [],
        "reports": [],
        "closed": False,
    }

    class DummyConn:
        def close(self):
            calls["closed"] = True

    def fake_gp_search(keyword, n_hits):
        calls["gp_search"] += 1
        return [{"app_id": "android-1", "app_name": "Android App"}]

    def fake_as_search(keyword, n_hits):
        calls["as_search"] += 1
        return [{"app_id": "ios-1", "app_name": "iOS App"}]

    def fake_gp_details(app_id):
        calls["gp_details"].append(app_id)
        return {"app_id": app_id, "store": "android", "description": "Android desc"}

    def fake_as_details(app_id):
        calls["as_details"].append(app_id)
        return {"app_id": app_id, "store": "ios", "description": "iOS desc"}

    def fake_generate_report(app_name, analysis_result, detailed):
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

    assert calls["gp_search"] == 1
    assert calls["as_search"] == 1
    assert calls["gp_details"] == ["android-1"]
    assert calls["as_details"] == ["ios-1"]
    assert [entry[2] for entry in calls["save_analysis"]] == ["android", "ios"]
    assert calls["closed"] is True