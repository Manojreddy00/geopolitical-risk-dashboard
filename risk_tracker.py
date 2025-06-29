import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
import time

# CONFIGURATION
API_KEY = "c96d48259e8947ee884b9b6eb3d34918"
OUTPUT_DIR = "news_data"
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')
SEVEN_DAYS_AGO = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%d')
OUTPUT_FILE = f"{OUTPUT_DIR}/geopolitical_news_{TODAY}.csv"
# EXPANDED KEYWORDS
KEYWORDS = [
    # Geopolitical
    'election', 'coup', 'protest', 'military', 'conflict', 'war', 'border', 'dispute',
    'missile', 'nuclear', 'terror', 'strike', 'sanctions', 'espionage', 'cyberattack',

    # Economic/Trade
    'tariff', 'trade war', 'inflation', 'interest rate', 'currency', 'deflation',
    'bank collapse', 'stock market crash', 'liquidity crisis', 'credit rating downgrade',

    # Energy & Commodities
    'oil', 'opec', 'gas', 'pipeline', 'embargo', 'energy prices',

    # Health & Climate
    'pandemic', 'covid', 'outbreak', 'quarantine', 'vaccine',
    'drought', 'flood', 'earthquake', 'climate change', 'heatwave',

    # Global Bodies
    'NATO', 'UN', 'BRICS', 'peace talks', 'summit', 'treaty',

    # Refugee & Migration
    'refugee', 'border crisis', 'migration', 'asylum seeker',

    # Tech Restrictions
    'chip ban', 'semiconductor', 'ai regulation', '5G ban', 'data privacy',

    # Leaders & Countries (contextual)
    'modi', 'biden', 'putin', 'xi jinping', 'zelenskyy',
    'china', 'russia', 'us', 'india', 'iran', 'israel', 'ukraine', 'taiwan'
]
# API SETUP
NEWS_API_URL = "https://newsapi.org/v2/everything"

PARAMS = {
    'from': SEVEN_DAYS_AGO,
    'to': TODAY,
    'language': 'en',
    'sortBy': 'publishedAt',
    'pageSize': 100,
    'apiKey': API_KEY
}

# FETCH FUNCTION
def fetch_articles(url, keyword_chunks, base_params):
    print(f"📡 Fetching news from {base_params['from']} to {base_params['to']}")
    all_articles = []

    for batch in keyword_chunks:
        base_params['q'] = ' OR '.join(batch)
        try:
            r = requests.get(url, params=base_params)
            r.raise_for_status()
            articles = r.json().get("articles", [])
            print(f"✅ Retrieved {len(articles)} articles for batch: {batch[:2]}...")
            all_articles.extend(articles)
        except Exception as e:
            print(f"❌ Error on batch {batch[:2]}: {e}")
        time.sleep(1)  # Be gentle with NewsAPI

    return all_articles

# PROCESS FUNCTION
def process_articles(articles):
    rows = []
    for article in articles:
        rows.append({
            'title': article.get('title'),
            'description': article.get('description'),
            'content': article.get('content'),
            'url': article.get('url'),
            'source': article.get('source', {}).get('name'),
            'published_at': article.get('publishedAt'),
            'collected_at': datetime.now(timezone.utc).isoformat()
        })
    return pd.DataFrame(rows)

# MAIN FUNCTION

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Chunk keywords into batches to avoid query length error
    chunk_size = 15
    keyword_chunks = [KEYWORDS[i:i + chunk_size] for i in range(0, len(KEYWORDS), chunk_size)]

    articles = fetch_articles(NEWS_API_URL, keyword_chunks, PARAMS)

    if not articles:
        print("⚠️ No articles fetched.")
        return

    df = process_articles(articles)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ {len(df)} articles saved to: {OUTPUT_FILE}")

# EXECUTE
if __name__ == "__main__":
    start = time.time()
    main()
    print(f"⏱️ Done in {round(time.time() - start, 2)} seconds.")
