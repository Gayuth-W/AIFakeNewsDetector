import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from rag_app.src.main import app
from rag_app.src.utils.llm_utils import parse_analysis_response


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_parse_analysis_response_json():
    raw = '{"prediction": "FAKE", "confidence": 0.92, "explanation": "False claim.", "key_claims": ["5G causes COVID"]}'
    result = parse_analysis_response(raw)
    assert result["prediction"] == "FAKE"
    assert result["confidence"] == 0.92
    assert result["key_claims"] == ["5G causes COVID"]


def test_parse_analysis_response_fallback():
    result = parse_analysis_response("This article appears to be FAKE based on the claims.")
    assert result["prediction"] == "FAKE"
    assert result["explanation"]


@patch("rag_app.src.services.fake_news_services.generate_response", new_callable=AsyncMock)
@patch("rag_app.src.services.fake_news_services.ArticleScraper.scrape")
@patch("rag_app.src.services.fake_news_services.retrieve_context")
def test_analyze_url(mock_retrieve, mock_scrape, mock_llm):
    mock_scrape.return_value = {
        "title": "Test Article",
        "text": "5G towers spread viruses.",
        "authors": ["Author"],
        "publish_date": "2024-01-01",
        "source_url": "https://example.com/article",
    }
    mock_retrieve.return_value = (
        "There is no scientific evidence supporting the claim that 5G spreads COVID-19.",
        ["There is no scientific evidence supporting the claim that 5G spreads COVID-19."],
    )
    mock_llm.return_value = (
        '{"prediction": "FAKE", "confidence": 0.95, '
        '"explanation": "Contradicts verified facts.", "key_claims": ["5G spreads viruses"]}'
    )

    response = client.post("/analyze-url?url=https://example.com/article")
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "FAKE"
    assert data["confidence"] == 0.95
    assert len(data["sources"]) == 1
    assert data["title"] == "Test Article"


@patch("rag_app.src.main.generate_response", new_callable=AsyncMock)
@patch("rag_app.src.main.retrieve_context")
def test_chat(mock_retrieve, mock_llm):
    mock_retrieve.return_value = ("Verified fact about vaccines.", ["Verified fact about vaccines."])
    mock_llm.return_value = "Vaccines are safe and effective."

    response = client.post(
        "/chat",
        json={"question": "Do vaccines cause autism?", "session_id": None, "model": "gemma3:1b"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["answer"] == "Vaccines are safe and effective."
    assert data["sources"] == ["Verified fact about vaccines."]


def test_session_not_found():
    response = client.get("/session/nonexistent-session-id")
    assert response.status_code == 404
