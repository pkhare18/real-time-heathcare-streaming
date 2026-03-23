from kafka import KafkaConsumer
import json
import duckdb
from config.config import KAFKA_BROKER, TOPIC
 
# Connect to DuckDB
conn = duckdb.connect("../healthcare.db")
 
# Create table
conn.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    doctor VARCHAR,
    rep VARCHAR,
    interaction_time TIMESTAMP
)
""")
 
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
 
    conn.execute(
        "INSERT INTO interactions VALUES (?, ?, ?)",
        (data['doctor'], data['rep'], data['interaction_time'])
    )
 
    print("Inserted:", data)
 