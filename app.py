import streamlit as st
from src.db import get_engine
from src.queries import (
    q_providers_receivers_by_city,
    q_top_provider_types_by_quantity,
    q_providers_contact_by_city,
    q_receivers_most_claims,
    q_total_food_available,
    q_top_cities_listings,
    q_common_food_types,
    q_claims_per_food_item,
    q_provider_highest_successful_claims,
    q_claims_status_percentages,
    q_avg_quantity_per_receiver,
    q_most_claimed_meal_type,
    q_total_quantity_by_provider,
)

st.set_page_config(page_title="Local Food Wastage Management", layout="wide")
st.title("Local Food Wastage Management System")
st.caption("Connect providers with receivers, reduce waste, and gain insights.")

engine = get_engine()

with st.sidebar:
    st.header("Filters")
    city = st.text_input("City (optional)")
    provider_type = st.selectbox("Provider Type", ["", "Restaurant", "Grocery Store", "Supermarket", "Bakery", "Other"])
    food_type = st.selectbox("Food Type", ["", "Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Meal Type", ["", "Breakfast", "Lunch", "Dinner", "Snacks"])

st.subheader("At a Glance")
col1, col2, col3 = st.columns(3)
with col1:
    df_total = q_total_food_available(engine, city_filter=city or None)
    st.metric("Total Quantity Available", int(df_total.iloc[0,0]) if not df_total.empty else 0)
with col2:
    df_cities = q_top_cities_listings(engine, limit=1)
    st.metric("Top City by Listings", df_cities.iloc[0,0] if not df_cities.empty else "—")
with col3:
    df_meal = q_most_claimed_meal_type(engine)
    st.metric("Most Claimed Meal Type", df_meal.iloc[0,0] if not df_meal.empty else "—")

st.subheader("Key Insights")
tabs = st.tabs([
    "Providers/Receivers by City",
    "Top Provider Types",
    "Providers Contacts",
    "Top Receivers by Claims",
    "Food Types",
    "Claims per Food Item",
    "Providers by Successful Claims",
    "Claim Status %",
    "Total by Provider",
])

with tabs[0]:
    st.dataframe(q_providers_receivers_by_city(engine), use_container_width=True)
with tabs[1]:
    st.dataframe(q_top_provider_types_by_quantity(engine), use_container_width=True)
with tabs[2]:
    st.dataframe(q_providers_contact_by_city(engine, city or None), use_container_width=True)
with tabs[3]:
    st.dataframe(q_receivers_most_claims(engine, limit=10), use_container_width=True)
with tabs[4]:
    st.dataframe(q_common_food_types(engine), use_container_width=True)
with tabs[5]:
    st.dataframe(q_claims_per_food_item(engine), use_container_width=True)
with tabs[6]:
    st.dataframe(q_provider_highest_successful_claims(engine, limit=10), use_container_width=True)
with tabs[7]:
    st.dataframe(q_claims_status_percentages(engine), use_container_width=True)
with tabs[8]:
    st.dataframe(q_total_quantity_by_provider(engine), use_container_width=True)

st.info("Explore more features in the Pages menu for CRUD and detailed views.")