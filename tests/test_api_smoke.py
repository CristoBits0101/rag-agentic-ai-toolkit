from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_health():
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert "service" in payload
    assert "version" in payload


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_v1_agent():
    response = client.get("/api/v1/agent/")
    assert response.status_code == 200
    assert "agent" in response.json()


def test_v1_chat():
    response = client.get("/api/v1/chat/")
    assert response.status_code == 200
    assert "chat" in response.json()


def test_v1_llm():
    response = client.get("/api/v1/llm/")
    assert response.status_code == 200
    assert "llm" in response.json()


def test_v1_rag():
    response = client.get("/api/v1/rag/")
    assert response.status_code == 200
    assert "rag" in response.json()


def test_v1_prompt_health():
    response = client.get("/api/v1/prompt/")
    assert response.status_code == 200
    assert "prompt" in response.json()
