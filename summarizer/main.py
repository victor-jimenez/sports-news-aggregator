import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class NewsSummarizer:
    def __init__(self):
        # Assumes GEMINI_API_KEY is in .env
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-3-flash-preview'
        print(f"Using model: {self.model_id}")
        print(f"API Key loaded: {api_key[:5]}...{api_key[-4:]}")

    def summarize_cluster(self, cluster):
        title = cluster['representative']['title']
        content = cluster['combined_content']
        articles = cluster['articles']
        sources = list(set([a['source'] for a in articles]))

        prompt = f"""
        You are a professional sports journalist. Your task is to create a combined summary of a news story based on reports from different sources.

        Story Title: {title}
        Sources: {', '.join(sources)}

        Combined Content:
        {content}

        Instructions:
        1. Create a concise summary (max 3-4 sentences).
        2. Merge the most important facts from all sources.
        3. Maintain a neutral, journalistic tone.
        4. If there are conflicting details, mention them briefly.
        5. Output only the summary text.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error summarizing story {title}: {e}")
            return "Summary unavailable due to an error."

    def process_all(self, input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as f:
            ranked_news = json.load(f)

        summarized_news = []
        # Limit to top 10 stories to avoid excessive API costs during testing
        for i, cluster in enumerate(ranked_news[:10]):
            print(f"Summarizing story {i+1}/{len(ranked_news[:10])}: {cluster['representative']['title']}")
            summary = self.summarize_cluster(cluster)

            summarized_news.append({
                "title": cluster['representative']['title'],
                "summary": summary,
                "sources": list(set([a['source'] for a in cluster['articles']])),
                "original_articles": [a['url'] for a in cluster['articles']]
            })

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summarized_news, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(summarized_news)} summaries to {output_file}")

def main():
    summarizer = NewsSummarizer()
    summarizer.process_all("processed_news.json", "summarized_news.json")

if __name__ == "__main__":
    main()
