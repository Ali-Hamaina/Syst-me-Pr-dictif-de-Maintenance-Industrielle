from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'RefrigerationStream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='refrigeration-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🧊 En attente de messages depuis Kafka (RefrigerationStream)...\n")

for message in consumer:
    data = message.value
    print(f"🛬 Données reçues: Machine {data['machine_id']}")
    print(f"   Mode: {data['operating_mode']}")
    print(f"   Température évaporateur: {data['temp_evaporator']}°C")
    print(f"   Température condenseur: {data['temp_condenser']}°C")
    print(f"   Pression haute: {data['pressure_high']} bar")
    print(f"   Pression basse: {data['pressure_low']} bar")
    print(f"   Surchauffe: {data['superheat']}°C")
    print(f"   Sous-refroidissement: {data['subcooling']}°C")
    print(f"   Courant compresseur: {data['compressor_current']}A")
    print(f"   Vibrations: {data['vibration']}g")
    print(f"   Efficacité: {data['efficiency']}")
    print("-" * 50)