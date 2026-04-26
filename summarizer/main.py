import json
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class NewsSummarizer:
    def __init__(self):
        # Assumes ANTHROPIC_API_KEY is in .env
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=300,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
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
