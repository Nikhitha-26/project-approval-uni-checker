import os
import requests
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util

SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # Set your SerpAPI key in environment variables

# Initialize Sentence-BERT model (you can choose a different model if needed)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def search_web_serpapi(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """Search the web using SerpAPI and return a list of results (title + snippet)."""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results,
        "engine": "google",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data.get("organic_results", []):
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        if title or snippet:
            results.append({"title": title, "snippet": snippet, "link": link})
    return results

def get_embedding(text: str):
    """Generate Sentence-BERT embedding for the given text."""
    return model.encode(text, convert_to_tensor=True)

def find_similar_projects(input_title: str, top_n: int = 5) -> List[Dict[str, Any]]:
    """Search web for project title, compare embeddings, and return top N similar results."""
    # Step 1: Search web
    results = search_web_serpapi(input_title, num_results=10)
    # Step 2: Generate embedding for input
    input_embedding = get_embedding(input_title)
    # Step 3: Generate embeddings for results and compute similarity
    similarities = []
    for result in results:
        combined_text = f"{result['title']} {result['snippet']}"
        result_embedding = get_embedding(combined_text)
        score = util.pytorch_cos_sim(input_embedding, result_embedding).item()
        similarities.append({
            "title": result["title"],
            "snippet": result["snippet"],
            "link": result["link"],
            "similarity": score
        })
    # Step 4: Sort and return top N
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_n]

# Example usage:
if __name__ == "__main__":
    title = "Deep Learning for Image Classification"
    top_results = find_similar_projects(title, top_n=3)
    for idx, res in enumerate(top_results, 1):
        print(f"{idx}. {res['title']} (Score: {res['similarity']:.3f})")
        print(f"   {res['snippet']}")
        print(f"   {res['link']}\n")