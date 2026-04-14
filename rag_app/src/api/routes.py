from fastapi import APIRouter, HTTPException

from rag_app.src.services.fake_news_services import FakeNewsService

router = APIRouter()


@router.post("/analyze-url")
async def analyze_news_url(url: str, model: str | None = None):
    try:
        return await FakeNewsService.analyze_from_url(url, model=model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
