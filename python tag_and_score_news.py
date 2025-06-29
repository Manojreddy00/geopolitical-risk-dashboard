import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re
from datetime import datetime

DATA_DIR = "news_data"
TODAY = datetime.now().strftime("%Y-%m-%d")
INPUT_FILE = f"{DATA_DIR}/geopolitical_news_{TODAY}.csv"
OUTPUT_FILE = f"{DATA_DIR}/geopolitical_news_tagged.csv"

analyzer = SentimentIntensityAnalyzer()
COUNTRY_KEYWORDS = {
    'United States': ['US', 'America', 'Biden', 'Trump', 'Washington'],
    'China': ['China', 'Beijing', 'Xi Jinping'],
    'Russia': ['Russia', 'Putin', 'Moscow'],
    'India': ['India', 'Modi', 'Delhi'],
    'Iran': ['Iran', 'Tehran'],
    'Ukraine': ['Ukraine', 'Kyiv'],
    'Israel': ['Israel', 'Netanyahu'],
    'Palestine': ['Palestine', 'Gaza'],
    'UK': ['UK', 'Britain', 'London', 'Sunak'],
    'European Union': ['EU', 'Brussels', 'France', 'Germany', 'Italy', 'Spain'],
    'Middle East': ['Middle East', 'Syria', 'Lebanon', 'Iraq', 'Yemen'],
    'South Korea': ['South Korea', 'Seoul'],
    'North Korea': ['North Korea', 'Kim Jong Un', 'Pyongyang'],
    'Japan': ['Japan', 'Tokyo', 'Kishida'],
    'Canada': ['Canada', 'Ottawa', 'Trudeau'],
    'Australia': ['Australia', 'Canberra', 'Albanese'],
}

CATEGORY_KEYWORDS = {
    'Political Instability': ['election', 'vote', 'resign', 'protest', 'coup'],
    'Conflict / War': ['strike', 'war', 'conflict', 'missile', 'airstrike', 'military'],
    'Civil Unrest / Terror': ['riot', 'terrorist', 'unrest', 'bombing'],
    'Sanctions / Trade': ['sanctions', 'tariff', 'embargo', 'trade war', 'ban', 'import', 'export'],
    'Cybersecurity': ['cyberattack', 'hack', 'espionage', 'malware'],
    'Energy Disruption': ['opec', 'oil', 'gas', 'pipeline', 'energy prices'],
    'Natural Disaster': ['earthquake', 'flood', 'wildfire', 'drought', 'storm'],
    'Health / Pandemic': ['covid', 'pandemic', 'virus', 'outbreak', 'quarantine'],
    'Currency / Financial': ['inflation', 'interest rate', 'currency', 'devaluation', 'rate hike', 'market crash'],
    'Alliances / Treaties': ['nato', 'treaty', 'un', 'brics', 'summit'],
    'Migration Crisis': ['refugee', 'asylum', 'border', 'migration'],
    'Tech Regulation': ['ban tiktok', 'ai ethics', 'chip ban', '5g ban', 'semiconductor'],
}

CATEGORY_TO_SECTOR = {
    'Political Instability': 'Government, Banking',
    'Conflict / War': 'Defense, Oil & Gas',
    'Civil Unrest / Terror': 'Insurance, Travel',
    'Sanctions / Trade': 'Manufacturing, Tech',
    'Cybersecurity': 'Tech, Finance',
    'Energy Disruption': 'Energy, Airlines',
    'Natural Disaster': 'Insurance, Agriculture',
    'Health / Pandemic': 'Healthcare, Pharma',
    'Currency / Financial': 'Banking, Forex',
    'Alliances / Treaties': 'Government, Defense',
    'Migration Crisis': 'Infrastructure, Housing',
    'Tech Regulation': 'Technology, Telecom',
}
def tag_country(text):
    for country, keywords in COUNTRY_KEYWORDS.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            return country
    return 'Unknown'

def tag_category(text):
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(re.search(rf'\b{re.escape(kw)}\b', text.lower()) for kw in keywords):
            return category
    return 'Uncategorized'

def tag_sector(category):
    return CATEGORY_TO_SECTOR.get(category, 'General')

def get_sentiment(text):
    if pd.isna(text):
        return 0.0
    return round(analyzer.polarity_scores(str(text))['compound'], 3)
def process_news(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return

    df = pd.read_csv(input_file)
    print(f"📄 Loaded {len(df)} articles")

    df['full_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')

    df['country'] = df['full_text'].apply(tag_country)
    df['category'] = df['full_text'].apply(tag_category)
    df['sector'] = df['category'].apply(tag_sector)
    df['sentiment_score'] = df['full_text'].apply(get_sentiment)

    df.drop(columns=['full_text'], inplace=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Tagged + Scored → {output_file}")

if __name__ == "__main__":
    process_news(INPUT_FILE, OUTPUT_FILE)
