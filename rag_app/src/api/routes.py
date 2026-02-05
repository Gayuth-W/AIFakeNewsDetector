from fastapi import APIRouter, HTTPException
from rag_app.src.services.fake_news_services import FakeNewsService

router = APIRouter()

@router.post("/analyze-url")
def analyze_news_url(url: str):
    try:
        return FakeNewsService.analyze_from_url(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))