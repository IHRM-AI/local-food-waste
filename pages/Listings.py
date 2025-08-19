import datetime as dt
import pandas as pd
import streamlit as st
from sqlalchemy import text
from src.db import get_engine

st.header("Food Listings (CRUD)")
engine = get_engine()

# Create
with st.expander("Add New Listing"):
    with st.form("add_listing"):
        food_name = st.text_input("Food Name", "")
        quantity = st.number_input("Quantity", min_value=1, step=1, value=10)
        expiry = st.date_input("Expiry Date", dt.date.today())
        provider_id = st.number_input("Provider ID", min_value=1, step=1)
        provider_type = st.text_input("Provider Type", "Restaurant")
        location = st.text_input("City", "")
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        submitted = st.form_submit_button("Create")
        if submitted:
            sql = """
            INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES ((SELECT COALESCE(MAX(Food_ID),0)+1 FROM food_listings), :n, :q, :e, :pid, :ptype, :loc, :ft, :mt)
            """
            with engine.begin() as con:
                con.execute(text(sql), {"n": food_name, "q": int(quantity), "e": expiry, "pid": int(provider_id),
                                        "ptype": provider_type, "loc": location, "ft": food_type, "mt": meal_type})
            st.success("Listing created.")

# Read + Update + Delete
st.subheader("All Listings")
df = pd.read_sql("SELECT * FROM food_listings ORDER BY Expiry_Date ASC", engine)
st.dataframe(df, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    del_id = st.number_input("Delete by Food_ID", min_value=0, step=1)
    if st.button("Delete"):
        with engine.begin() as con:
            con.execute(text("DELETE FROM claims WHERE Food_ID=:id"), {"id": int(del_id)})
            con.execute(text("DELETE FROM food_listings WHERE Food_ID=:id"), {"id": int(del_id)})
        st.success(f"Deleted listing {int(del_id)}")

with col2:
    upd_id = st.number_input("Update Quantity for Food_ID", min_value=0, step=1, key="upd_id")
    new_q = st.number_input("New Quantity", min_value=0, step=1, key="upd_q")
    if st.button("Update Quantity"):
        with engine.begin() as con:
            con.execute(text("UPDATE food_listings SET Quantity=:q WHERE Food_ID=:id"), {"q": int(new_q), "id": int(upd_id)})
        st.success(f"Updated quantity for {int(upd_id)}")

with col3:
    st.info("Use Provider_ID from Providers page to link new listings.")