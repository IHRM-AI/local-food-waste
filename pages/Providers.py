import pandas as pd
import streamlit as st
from sqlalchemy import text
from src.db import get_engine

st.header("Providers")
engine = get_engine()

df = pd.read_sql("SELECT * FROM providers ORDER BY City, Name", engine)
st.dataframe(df, use_container_width=True)

with st.expander("Add Provider"):
    with st.form("add_provider"):
        name = st.text_input("Name")
        ptype = st.text_input("Type", "Restaurant")
        address = st.text_area("Address")
        city = st.text_input("City")
        contact = st.text_input("Contact")
        if st.form_submit_button("Create"):
            sql = """
            INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact)
            VALUES ((SELECT COALESCE(MAX(Provider_ID),0)+1 FROM providers), :n, :t, :a, :c, :ct)
            """
            with engine.begin() as con:
                con.execute(text(sql), {"n": name, "t": ptype, "a": address, "c": city, "ct": contact})
            st.success("Provider added.")