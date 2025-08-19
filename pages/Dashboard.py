import streamlit as st
import plotly.express as px
from src.db import get_engine
from src.queries import q_top_cities_listings, q_common_food_types

st.header("Dashboard")
engine = get_engine()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Listings by City")
    df_cities = q_top_cities_listings(engine, limit=50)
    if not df_cities.empty:
        fig = px.bar(df_cities, x="city", y="listings")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data.")

with col2:
    st.subheader("Available Food by Type")
    df_types = q_common_food_types(engine)
    if not df_types.empty:
        fig = px.pie(df_types, values="total_quantity", names="food_type")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data.")