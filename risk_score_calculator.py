import pandas as pd
INPUT_FILE = "news_data/geopolitical_news_tagged.csv"
OUTPUT_FILE = "news_data/geopolitical_news_scored.csv"
CATEGORY_RISK = {
    'Conflict / War': 50,
    'Civil Unrest / Terror': 45,
    'Sanctions / Trade': 40,
    'Cybersecurity': 35,
    'Political Instability': 30,
    'Energy Disruption': 30,
    'Health / Pandemic': 25,
    'Currency / Financial': 25,
    'Natural Disaster': 25,
    'Migration Crisis': 20,
    'Alliances / Treaties': 15,
    'Tech Regulation': 15,
    'Uncategorized': 10
}
COUNTRY_BASELINE = {
    'Russia': 15,
    'Ukraine': 15,
    'Iran': 15,
    'Israel': 15,
    'Middle East': 15,
    'Palestine': 15,
    'China': 10,
    'India': 10,
    'United States': 8,
    'European Union': 8,
    'UK': 7,
    'Unknown': 5
}
DEFAULT_COUNTRY_RISK = 6
def calculate_risk_score(row):
    try:
        sentiment_score = float(row.get('sentiment_score', 0))
    except:
        sentiment_score = 0.0

    sentiment_penalty = max(0, round(-sentiment_score * 30))  # Negative sentiment adds risk
    category_risk = CATEGORY_RISK.get(row.get('category', 'Uncategorized'), 10)
    country_risk = COUNTRY_BASELINE.get(row.get('country', 'Unknown'), DEFAULT_COUNTRY_RISK)

    raw_score = sentiment_penalty + category_risk + country_risk
    return min(raw_score, 100)
def apply_risk_scores(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    df = pd.read_csv(input_file)
    print(f"📄 Loaded {len(df)} tagged articles")

    df['risk_score'] = df.apply(calculate_risk_score, axis=1)
    df.sort_values(by='risk_score', ascending=False, inplace=True)

    df.to_csv(output_file, index=False)
    print(f"✅ Risk scores saved to → {output_file}")

    # Optional summary logging
    top_countries = df['country'].value_counts().head(5).to_dict()
    print(f"🌍 Top 5 countries in data: {top_countries}")
    print("📊 Top 5 risk articles:")
    print(df[['title', 'country', 'category', 'risk_score']].head(5))

if __name__ == "__main__":
    import os
    apply_risk_scores(INPUT_FILE, OUTPUT_FILE)
