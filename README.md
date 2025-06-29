# Geopolitical Risk Intelligence Dashboard

A real-time, interactive dashboard that ingests global news, analyzes geopolitical risk using sentiment and category scoring, and visualizes insights by country and sector. Built to support financial risk monitoring, market analysis, and strategic decision-making.
##  Overview
This dashboard:
- Pulls global news using **NewsAPI** based on 50+ geopolitical keywords
- Tags articles by **country**, **event category**, and **economic sector**
- Analyzes **sentiment** using VADER
- Calculates a **custom risk score** based on sentiment, event type, and baseline country risk
- Visualizes insights via **Streamlit + Plotly** with maps, charts, and filters
##  Key Features
-  **Real-Time News Fetch**: Pulls and processes articles from the past 7 days
-  **Tagging System**: Automatically tags articles by country and geopolitical category
-  **Sentiment Analysis**: Uses VADER to assess sentiment of each article
-  **Risk Scoring**: Combines category weights, country volatility, and sentiment to generate a composite risk score
-  **Dashboard Visualizations**:
  - Time-series risk & sentiment trends
  - Risk choropleth map by country
  - Sector × Country risk heatmap
  - Histogram by category
  - Filterable and downloadable article feed
## Tech Stack
- **Backend**: Python, Pandas, VADER, NewsAPI
- **Frontend**: Streamlit, Plotly
- **Visualization**: Line charts, bar graphs, choropleth maps, heatmaps
Future Scope
Advanced Sentiment Modeling: Replace VADER with domain-specific models like FinBERT or transformer-based sentiment classifiers for more accurate analysis of financial and geopolitical language.
Market Correlation Analysis: Compare risk scores against real market indicators like the VIX, MSCI EM Index, or country ETFs to validate and improve the scoring model.
Live Scheduled Pipelines: Automate daily fetching and scoring using cron jobs, Airflow, or GitHub Actions, enabling true real-time monitoring.
Alerts & Risk Spikes: Add a rule-based or ML-driven alert system that flags sudden surges in risk for a specific country or sector.
