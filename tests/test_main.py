"""第 0 周冒烟测试：确认依赖装好、应用能起来。

运行：uv run pytest -v
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_ok() -> None:
    """根路径应该返回 200 且 app 名字正确。"""
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["app"] == "fitness-ai"
    assert body["status"] == "ok"


def test_health_ok() -> None:
    """健康检查接口应该返回 healthy。"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}
