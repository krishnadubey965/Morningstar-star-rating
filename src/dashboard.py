import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('data/final_ratings.csv')

df = load_data()

# Page setup
st.set_page_config(page_title="Morningstar Rating Engine", page_icon="⭐", layout="wide")

st.title("⭐ Morningstar Star Rating Replication Engine")
st.markdown("*Replicating Morningstar's MRAR-based fund rating model*")

st.divider()

# Sidebar filters
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Category", ["All"] + list(df['category'].unique()))
min_stars = st.sidebar.slider("Minimum Stars", 1, 5, 1)

# Filter data
filtered = df.copy()
if category != "All":
    filtered = filtered[filtered['category'] == category]
filtered = filtered[filtered['stars'] >= min_stars]

# Top metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Funds", len(filtered))
col2.metric("5 Star Funds", len(filtered[filtered['stars']==5]))
col3.metric("Avg MRAR", f"{filtered['combined_mrar'].mean():.2f}%")

st.divider()

# Leaderboard
st.subheader("🏆 Fund Leaderboard")
display_df = filtered[['fund_name','category','mrar_3yr','mrar_5yr','combined_mrar','stars']].sort_values('stars', ascending=False)
display_df['stars'] = display_df['stars'].apply(lambda x: '⭐'*int(x))
st.dataframe(display_df, use_container_width=True)

st.divider()

# Charts side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Star Distribution")
    fig1 = px.histogram(filtered, x='stars', color='category',
                       barmode='group',
                       title="Funds per Star Rating")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 MRAR Comparison")
    fig2 = px.bar(filtered.sort_values('combined_mrar', ascending=True),
                  x='combined_mrar', y='fund_name',
                  color='category', orientation='h',
                  title="MRAR Score by Fund")
    st.plotly_chart(fig2, use_container_width=True)
    