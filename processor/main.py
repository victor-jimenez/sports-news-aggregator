import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime

class NewsProcessor:
    def __init__(self, similarity_threshold=0.3):
        self.similarity_threshold = similarity_threshold

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def cluster_articles(self, df):
        """
        Groups articles based on title similarity using TF-IDF and Cosine Similarity.
        """
        if df.empty:
            return []

        # We use the title for clustering
        titles = df['title'].tolist()
        vectorizer = TfidfVectorizer(stop_words='english') # In a real scenario, use Spanish stop words
        tfidf_matrix = vectorizer.fit_transform(titles)

        similarity_matrix = cosine_similarity(tfidf_matrix)

        visited = set()
        clusters = []

        for i in range(len(titles)):
            if i in visited:
                continue

            # Start a new cluster
            current_cluster = [i]
            visited.add(i)

            for j in range(i + 1, len(titles)):
                if j not in visited and similarity_matrix[i][j] > self.similarity_threshold:
                    current_cluster.append(j)
                    visited.add(j)

            clusters.append(current_cluster)

        return clusters

    def rank_clusters(self, df, clusters):
        """
        Ranks clusters based on the number of unique sources and average title length/prominence.
        """
        ranked_clusters = []

        for cluster_indices in clusters:
            cluster_df = df.iloc[cluster_indices]

            # Score based on number of sources
            num_sources = cluster_df['source'].nunique()

            # Score based on the number of articles in the cluster
            num_articles = len(cluster_df)

            # Total score: more sources + more articles = higher relevance
            score = (num_sources * 2) + num_articles

            # Representative article (usually the one from the most prominent source or first found)
            representative = cluster_df.iloc[0].to_dict()

            # Combine all content for later summarization
            combined_content = " ".join(cluster_df['content'].fillna("").astype(str).tolist())

            ranked_clusters.append({
                "representative": representative,
                "articles": cluster_df.to_dict('records'),
                "score": score,
                "combined_content": combined_content
            })

        # Sort by score descending
        ranked_clusters.sort(key=lambda x: x['score'], reverse=True)
        return ranked_clusters

def main():
    processor = NewsProcessor()
    try:
        df = processor.load_data("scraped_news.csv")
        print(f"Processing {len(df)} articles...")

        clusters = processor.cluster_articles(df)
        print(f"Found {len(clusters)} clusters.")

        ranked_news = processor.rank_clusters(df, clusters)

        # Save results for the summarizer
        import json
        with open("processed_news.json", "w", encoding="utf-8") as f:
            json.dump(ranked_news, f, ensure_ascii=False, indent=2)

        print("Processed news saved to processed_news.json")

        # Print top 3 stories
        for i, story in enumerate(ranked_news[:3]):
            print(f"\nStory {i+1} (Score: {story['score']}):")
            print(f"Title: {story['representative']['title']}")
            print(f"Sources: {len(story['articles'])}")

    except FileNotFoundError:
        print("Error: scraped_news.csv not found. Run the scraper first.")

if __name__ == "__main__":
    main()
