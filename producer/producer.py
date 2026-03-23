from kafka import KafkaProducer
import json
import time
import random
 
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
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
 
    producer.send("doctor_interactions", value=data) # topic name will be doctor_interactions
    print(f"Sent: {data}")
 
    time.sleep(2)