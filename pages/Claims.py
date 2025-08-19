import pandas as pd
import streamlit as st
from sqlalchemy import text
from src.db import get_engine

st.header("Claims")
engine = get_engine()

df = pd.read_sql("""
SELECT c.Claim_ID, c.Food_ID, fl.Food_Name, c.Receiver_ID, r.Name AS Receiver_Name, c.Status, c.Timestamp
FROM claims c
JOIN receivers r ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings fl ON fl.Food_ID = c.Food_ID
ORDER BY c.Timestamp DESC
""", engine)
st.dataframe(df, use_container_width=True)

with st.expander("Add Claim"):
    with st.form("add_claim"):
        food_id = st.number_input("Food_ID", min_value=1, step=1)
        receiver_id = st.number_input("Receiver_ID", min_value=1, step=1)
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        ts = st.datetime_input("Timestamp")
        if st.form_submit_button("Create"):
            sql = """
            INSERT INTO claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp)
            VALUES ((SELECT COALESCE(MAX(Claim_ID),0)+1 FROM claims), :fid, :rid, :s, :ts)
            """
            with engine.begin() as con:
                con.execute(text(sql), {"fid": int(food_id), "rid": int(receiver_id), "s": status, "ts": ts})
            st.success("Claim added.")