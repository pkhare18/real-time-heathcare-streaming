from kafka import KafkaConsumer
import json
from config.config import KAFKA_BROKER, TOPIC
 
# To be replaced with postgresql
 
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
 