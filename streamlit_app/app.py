import streamlit as st
from kafka import KafkaConsumer
import json
from collections import defaultdict
 
st.set_page_config(page_title="Healthcare Streaming Dashboard")
 
st.title("Real-Time Healthcare Interaction Dashboard")
 
consumer = KafkaConsumer(
    'doctor_interactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='streamlit-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
 
doctor_counts = defaultdict(int)
rep_counts = defaultdict(int)
total = 0
 
placeholder = st.empty()
 
for message in consumer:
    data = message.value
    print(data)
    doctor = data["doctor"]
    rep = data["rep"]
    
    doctor_counts[doctor] += 1
    rep_counts[rep] += 1
    total += 1
 
    with placeholder.container():
        st.metric("Total Interactions", total)
        st.write("Last event: ",data)
        st.subheader("Interactions per Doctor")
        st.bar_chart(dict(doctor_counts))
        
        st.subheader("Interactions per Rep")
        st.bar_chart(dict(rep_counts))