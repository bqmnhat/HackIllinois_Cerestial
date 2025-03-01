import time
import random
import urllib.request
from urllib.error import HTTPError
from rag_scraper.scraper import Scraper
from rag_scraper.converter import Converter
from googlesearch import search
from rank_bm25 import BM25Okapi
import re

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    # Add more User-Agents here
]

def scrape_and_rank(query, num_results=10):
    urls = list(search(query, num=num_results))
    corpus = []
    results = []

    for url in urls:
        try:
            user_agent = random.choice(user_agents)
            headers = {"User-Agent": user_agent}
            html_content = Scraper.fetch_html(url, headers=headers)

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
            else:
                print(f"Failed to fetch HTML from {url}")

        except HTTPError as e:
            if e.code == 429:
                print(f"429 Error: Too Many Requests for {url}. Retrying after delay.")
                time.sleep(random.uniform(10, 30)) # Wait between 10 to 30 seconds.
                try:
                    user_agent = random.choice(user_agents)
                    headers = {"User-Agent": user_agent}
                    html_content = Scraper.fetch_html(url, headers=headers)

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
                    else:
                        print(f"Failed to fetch HTML from {url} after retry.")

                except Exception as inner_e:
                    print(f"Error processing {url} during retry: {inner_e}")
            else:
                print(f"HTTP Error {e.code} for {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

        time.sleep(random.uniform(1, 3)) # Delay between 1 to 3 seconds between requests

    if not corpus:
        print("No content to rank.")
        return

    bm25 = BM25Okapi(corpus)
    tokenized_query = query.lower().split()
    doc_scores = bm25.get_scores(tokenized_query)
    ranked_results = sorted(zip(doc_scores, results), key=lambda x: x[0], reverse=True)

    with open("output.txt", "w", encoding="utf-8") as f:
        for score, result in ranked_results:
            f.write(f"URL: {result['url']}\n")
            f.write(f"Score: {score}\n")
            f.write(f"Text:\n{result['text']}\n")
            f.write("-" * 40 + "\n")

if __name__ == "__main__":
    query = "tools or resources to help farmers assess their soil's water-holding capacity"
    scrape_and_rank(query)