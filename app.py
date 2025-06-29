import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

st.set_page_config(page_title="Geopolitical Risk Dashboard", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("news_data/geopolitical_news_scored.csv")
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')
    df.dropna(subset=['published_at'], inplace=True)
    return df

df = load_data()

st.sidebar.header("🔎 Filter News")

all_countries = sorted(df['country'].dropna().unique())
all_categories = sorted(df['category'].dropna().unique())

select_all_countries = st.sidebar.checkbox("Select All Countries", value=True)
selected_countries = all_countries if select_all_countries else st.sidebar.multiselect("Country", all_countries)

select_all_categories = st.sidebar.checkbox("Select All Categories", value=True)
selected_categories = all_categories if select_all_categories else st.sidebar.multiselect("Category", all_categories)
today = df['published_at'].max().date()
start_day = today - timedelta(days=6)

daily_df = df[
    (df['published_at'].dt.date >= start_day) &
    (df['published_at'].dt.date <= today) &
    (df['country'].isin(selected_countries)) &
    (df['category'].isin(selected_categories))
].copy()

daily_df['date'] = daily_df['published_at'].dt.date
st.title("🌍 Geopolitical Risk Intelligence Dashboard")
st.markdown("Live global insights from news tagged by country, sector, and risk. Focused on the last 7 days.")

col1, col2, col3 = st.columns(3)
col1.metric("📰 Articles (7 days)", len(daily_df))
col2.metric("🌐 Countries", daily_df['country'].nunique())
col3.metric("⚠️ Avg. Risk Score", round(daily_df['risk_score'].mean(), 2) if len(daily_df) > 0 else "N/A")
st.subheader("📅 Risk & Article Trends (Last 7 Days)")

trend_daily = daily_df.groupby('date').agg({
    'risk_score': 'mean',
    'sentiment_score': 'mean',
    'title': 'count'
}).reset_index().rename(columns={'title': 'article_count'})

fig_line = px.line(trend_daily, x='date', y=['risk_score', 'sentiment_score'],
                   markers=True,
                   title="Daily Avg. Risk & Sentiment",
                   labels={'value': 'Score', 'date': 'Date'})

fig_bar = px.bar(trend_daily, x='date', y='article_count',
                 title="🗓️ Articles Published per Day",
                 color_discrete_sequence=['#636EFA'],
                 labels={'article_count': 'Articles', 'date': 'Date'})

col1, col2 = st.columns(2)
col1.plotly_chart(fig_line, use_container_width=True)
col2.plotly_chart(fig_bar, use_container_width=True)
st.subheader("🗺️ Risk by Country (Last 7 Days)")

map_data = daily_df.groupby('country')['risk_score'].mean().reset_index()
fig_map = px.choropleth(
    map_data,
    locations='country',
    locationmode='country names',
    color='risk_score',
    color_continuous_scale='OrRd',
    title="Average Risk Score by Country",
)
fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth',
        bgcolor='rgba(0,0,0,0)'
    )
)
st.plotly_chart(fig_map, use_container_width=True)
st.subheader("🏭 Sector × Country Risk Heatmap")

heatmap_df = daily_df.pivot_table(index='sector', columns='country',
                                  values='risk_score', aggfunc='mean').fillna(0)

if not heatmap_df.empty:
    fig_heat = px.imshow(heatmap_df,
                         labels=dict(x="Country", y="Sector", color="Avg. Risk"),
                         color_continuous_scale="Reds",
                         aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("📭 Not enough data to display heatmap.")
st.subheader("📊 Risk Score Distribution by Category")

if len(daily_df) > 0:
    fig_hist = px.histogram(daily_df, x='risk_score', color='category',
                            nbins=25, barmode='stack',
                            title="Risk Score Histogram")
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("⚠️ No data to show.")
st.subheader("🧠 Top Risk Articles (Last 7 Days)")
top_df = daily_df.sort_values(by='risk_score', ascending=False).head(15)
st.dataframe(top_df[['published_at', 'title', 'country', 'category', 'sector', 'risk_score']],
             use_container_width=True)
csv = daily_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered News (CSV)", data=csv,
                   file_name="geopolitical_news_last7days.csv", mime='text/csv')
