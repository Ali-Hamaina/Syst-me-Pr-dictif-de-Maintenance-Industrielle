from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'Stream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='test-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🟢 En attente de messages depuis Kafka...\n")

for message in consumer:
    print(f"🛬 Message reçu: {message.value}")