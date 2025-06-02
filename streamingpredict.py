import pickle
import pandas as pd
import os
import requests
from datetime import datetime
import time
import json
from kafka import KafkaConsumer

# 📦 Chargement du modèle ML avec chemin dynamique
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_logistic.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Modèle chargé avec succès")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    exit(1)

# Configuration Flask endpoint
FLASK_ENDPOINT = "http://localhost:5000/api/prediction"

# Create Kafka consumer
consumer = KafkaConsumer(
    'Stream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='prediction-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🚀 Streaming prediction service started - sending data to Flask dashboard")
print("📊 Dashboard URL: http://localhost:5000")
print("⏳ Waiting for messages from Kafka...\n")

# Process messages from Kafka
for message in consumer:
    try:
        record = message.value
        
        # Send to Flask API
        response = requests.post(FLASK_ENDPOINT, json=record, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Record sent to Flask: Machine #{record['machine_id']} at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"❌ Error sending to Flask API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error processing record: {e}")


