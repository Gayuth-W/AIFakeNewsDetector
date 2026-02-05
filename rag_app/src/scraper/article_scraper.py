from newspaper import Article

class ArticleScraper:
    @staticmethod
    def scrape(url: str) -> dict:
        try:
            article = Article(url)
            article.download()
            article.parse()

            if not article.text:
                raise ValueError("No article text found")

            return {
                "title": article.title,
                "text": article.text,
                "authors": article.authors,
                "publish_date": str(article.publish_date),
                "source_url": url
            }

        except Exception as e:
            raise RuntimeError(f"Scraping failed: {str(e)}")
