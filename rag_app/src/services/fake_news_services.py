from rag_app.src.scraper.article_scraper import ArticleScraper

class FakeNewsService:
    @staticmethod
    def analyze_from_url(url: str):
        article_data = ArticleScraper.scrape(url)

        article_text = article_data["text"]

        # 🔮 Your ML model logic here
        prediction = "FAKE"  # placeholder
        confidence = 0.87

        return {
            "title": article_data["title"],
            "prediction": prediction,
            "confidence": confidence
        }