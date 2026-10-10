from __future__ import annotations

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_ask_endpoint_works():
    response = client.post('/ask', json={'question': 'What is the liability cap in the MSA?', 'strategy': 'heading_aware'})
    assert response.status_code == 200
    payload = response.json()
    assert 'answer' in payload
    assert isinstance(payload['sources'], list)
