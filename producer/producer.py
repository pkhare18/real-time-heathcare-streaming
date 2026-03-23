from kafka import KafkaProducer
import json
import time
import random
from config.config import KAFKA_BROKER,TOPIC
 
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
 
doctors = ["Dr. Smith", "Dr. John", "Dr. Lee"]
reps = ["Rep A", "Rep B", "Rep C"]
 
while True:
    data = {
        "doctor": random.choice(doctors),
        "rep": random.choice(reps),
        "interaction_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
 
    producer.send(TOPIC, value=data) # topic name will be doctor_interactions
    print(f"Sent: {data}")
 
    time.sleep(2)