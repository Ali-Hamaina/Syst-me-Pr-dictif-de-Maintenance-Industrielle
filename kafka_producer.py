from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "machine_id": random.randint(1, 5),
        "volt": round(random.uniform(10.0, 15.0), 2),
        "rotate": round(random.uniform(20.0, 30.0), 2),
        "pressure": round(random.uniform(70.0, 90.0), 2),
        "vibration": round(random.uniform(0.5, 2.0), 2)
    }

while True:
    data = generate_data()
    print(f"➡️ Sending: {data}")
    producer.send('Stream', value=data)
    time.sleep(2)