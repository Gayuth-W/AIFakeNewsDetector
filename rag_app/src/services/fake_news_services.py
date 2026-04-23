from rag_app.src.core.llm import generate_response, OLLAMA_MODEL
from rag_app.src.rag.rag_pipeline import retrieve_context
from rag_app.src.scraper.article_scraper import ArticleScraper
from rag_app.src.utils.llm_utils import parse_analysis_response

ARTICLE_TEXT_LIMIT = 3000

ANALYSIS_SYSTEM_PROMPT = """You are a fact-checking assistant that evaluates news articles for misinformation.

Use the verified reference information when it is relevant to the article's claims.
If the reference information does not cover the article, say so and base your assessment on general reasoning.

Respond ONLY with valid JSON in this exact format:
{
  "prediction": "REAL" | "FAKE" | "MIXED" | "UNVERIFIABLE",
  "confidence": 0.0 to 1.0,
  "explanation": "Brief explanation of your verdict",
  "key_claims": ["claim 1", "claim 2"]
}

Prediction meanings:
- REAL: claims appear accurate and well-supported
- FAKE: contains demonstrably false or misleading claims
- MIXED: contains both accurate and false/misleading claims
- UNVERIFIABLE: not enough evidence to determine accuracy"""


class FakeNewsService:
    @staticmethod
    async def analyze_from_url(url: str, model: str | None = None):
        article_data = ArticleScraper.scrape(url)
        article_text = article_data["text"][:ARTICLE_TEXT_LIMIT]

        rag_query = f"{article_data['title']}. {article_text}"
        context, sources = retrieve_context(rag_query, k=5)

        context_block = context if context else "No matching verified facts found in the knowledge base."

        user_prompt = (
            f"Article title: {article_data['title']}\n"
            f"Source URL: {url}\n\n"
            f"Verified reference information:\n{context_block}\n\n"
            f"Article text:\n{article_text}\n\n"
            "Analyze this article and return your JSON verdict."
        )

        messages = [
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        raw_response = await generate_response(messages, model=model or OLLAMA_MODEL)
        analysis = parse_analysis_response(raw_response)

        return {
            "title": article_data["title"],
            "source_url": url,
            "authors": article_data["authors"],
            "publish_date": article_data["publish_date"],
            "prediction": analysis["prediction"],
            "confidence": analysis["confidence"],
            "explanation": analysis["explanation"],
            "key_claims": analysis["key_claims"],
            "sources": sources,
        }
