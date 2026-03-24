from kafka import KafkaConsumer
import json
import psycopg2
from config.config import KAFKA_BROKER, TOPIC
from dotenv import load_dotenv
import os
 
load_dotenv()

# To be replaced with postgresql
conn=psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
) 

cursor=conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    doctor TEXT,
    rep TEXT,
    interaction_time TIMESTAMP
)
""")

conn.commit()

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    group_id='db-writer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
 
print("Processor started...")
 
for message in consumer:
    data = message.value
 
    cursor.execute(
        "INSERT INTO interactions VALUES (%s, %s, %s)",
        (data['doctor'], data['rep'], data['interaction_time'])
    )
    conn.commit()
 
    print("Inserted:", data)
 