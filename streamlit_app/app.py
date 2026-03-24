import streamlit as st
import psycopg2
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()
# Page config
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
 
st.title("📊 Real-Time Healthcare Interaction Dashboard")
 
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
) 
 
# Auto refresh every 5 seconds
refresh_interval = 5

while True:
    try:
        query_total = "SELECT COUNT(*) FROM interactions"
        total = pd.read_sql(query_total, conn).iloc[0, 0]
 
        st.metric("Total Interactions", total)
 
        query_doctor = """
            SELECT doctor, COUNT(*) as count
            FROM interactions
            GROUP BY doctor
        """
        doctor_df = pd.read_sql(query_doctor, conn)
 
        st.subheader("Interactions per Doctor")
        st.bar_chart(doctor_df.set_index("doctor"))
 
        query_rep = """
            SELECT rep, COUNT(*) as count
            FROM interactions
            GROUP BY rep
        """
        rep_df = pd.read_sql(query_rep, conn)
 
        st.subheader("Interactions per Rep")
        st.bar_chart(rep_df.set_index("rep"))
 
    except Exception as e:
        st.warning("Waiting for data...")
 
    time.sleep(refresh_interval)
    st.rerun()