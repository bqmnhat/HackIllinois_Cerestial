import urllib.request
from urllib.error import HTTPError
import time
import random
from rag_scraper.converter import Converter
from googlesearch import search
from rank_bm25 import BM25Okapi
import re
from urllib.error import HTTPError
import os

def fetch_html_with_headers(url, headers=None):
    try:
        req = urllib.request.Request(url, headers=headers or {})
        # Extract the URL string from the request object
        url_string = req.full_url
        with urllib.request.urlopen(url_string) as response:
            return response.read().decode('utf-8')
    except HTTPError as e:
        raise e
    except Exception as e:
        raise e
    
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    # Add more User-Agents here
]

def scrape_and_rank(query, num_results=10):
    urls = search(query, stop=num_results)
    corpus = []
    results = []
    processed_count = 0

    for url in urls:
        processed_count += 1
        print(f"Processing URL: {url}")  # Status print

        try:
            user_agent = random.choice(user_agents)
            headers = {"User-Agent": user_agent}

            try:
                html_content = fetch_html_with_headers(url, headers=headers)
            except HTTPError as e:
                if e.code == 429:
                    print(f"429 Error: Too Many Requests for {url}. Retrying after delay.")
                    time.sleep(random.uniform(10, 30))
                    html_content = fetch_html_with_headers(url, headers=headers)
                else:
                    raise e

            if html_content:
                markdown_content = Converter.html_to_markdown(
                    html=html_content,
                    base_url=url,
                    parser_features='html.parser',
                    ignore_links=True
                )
                text_content = re.sub(r'\s+', ' ', markdown_content).strip()
                corpus.append(text_content.lower().split())
                results.append({"url": url, "text": text_content})
                print(f"Successfully processed {url}") #status print
            else:
                print(f"Failed to fetch HTML from {url}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

        time.sleep(random.uniform(1, 3))

    if not corpus:
        print("No content to rank.")
        return

    bm25 = BM25Okapi(corpus)
    tokenized_query = query.lower().split()
    doc_scores = bm25.get_scores(tokenized_query)
    ranked_results = sorted(zip(doc_scores, results), key=lambda x: x[0], reverse=True)

    with open(os.getenv("SCRAPE_CONTEXT_PATH"), "w", encoding="utf-8") as f:
        print("Writing results to output.txt...") #Status print
        for score, result in ranked_results:
            f.write(f"URL: {result['url']}\n")
            f.write(f"Score: {score}\n")
            f.write(f"Text:\n{result['text']}\n")
            f.write("-" * 40 + "\n")
        print("Results written successfully.") #Status print

def updateScrapeData():
    query = "tools or resources to help farmers assess their soil's water-holding capacity"
    scrape_and_rank(query, 5)