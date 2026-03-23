from kafka import KafkaConsumer
import json
 
consumer = KafkaConsumer(
    'doctor_interactions', #topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='healthcare-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
 
print("Consumer started...")
 
for message in consumer:
    data = message.value
    print(f"Received: {data}")