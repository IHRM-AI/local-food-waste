import streamlit as st
from src.db import get_engine
from src.queries import (
    q_avg_quantity_per_receiver,
    q_most_claimed_meal_type,
    q_claims_status_percentages,
)

st.header("Insights")
engine = get_engine()

st.subheader("Average Quantity per Receiver")
st.dataframe(q_avg_quantity_per_receiver(engine), use_container_width=True)

st.subheader("Most Claimed Meal Type")
st.dataframe(q_most_claimed_meal_type(engine), use_container_width=True)

st.subheader("Claim Status Breakdown")
st.dataframe(q_claims_status_percentages(engine), use_container_width=True)