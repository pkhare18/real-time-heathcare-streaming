import streamlit as st
import duckdb
import time
 
# Page config
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
 
st.title("📊 Real-Time Healthcare Interaction Dashboard")
 
# Connect to DuckDB
conn = duckdb.connect("../healthcare.db")
 
# Auto refresh every 5 seconds
refresh_interval = 5
placeholder = st.empty()
 
while True:
    with placeholder.container():
 
        # Total interactions
        total = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
        st.metric("Total Interactions", total)
 
        col1, col2 = st.columns(2)
 
        # Doctor Aggregation
        doctor_df = conn.execute("""
            SELECT doctor, COUNT(*) as count
            FROM interactions
            GROUP BY doctor
            ORDER BY count DESC
        """).df()
 
        with col1:
            st.subheader("👨‍⚕️ Interactions per Doctor")
            st.bar_chart(doctor_df.set_index("doctor"))
 
        # Rep Aggregation
        rep_df = conn.execute("""
            SELECT rep, COUNT(*) as count
            FROM interactions
            GROUP BY rep
            ORDER BY count DESC
        """).df()
 
        with col2:
            st.subheader("🧑‍💼 Interactions per Rep")
            st.bar_chart(rep_df.set_index("rep"))
 
        # Latest records (optional but useful)
        st.subheader("📌 Latest Interactions")
        latest_df = conn.execute("""
            SELECT *
            FROM interactions
            ORDER BY interaction_time DESC
            LIMIT 5
        """).df()
 
        st.dataframe(latest_df)
 
    time.sleep(refresh_interval)