from kafka import KafkaProducer
import json
import time
import random
import numpy as np

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_refrigeration_data():
    """Génère des données de capteurs pour installations frigorifiques"""
    
    # Simulation de différentes conditions de fonctionnement
    operating_modes = ["normal", "high_load", "low_load", "defrost", "startup"]
    mode = random.choice(operating_modes)
    
    # Génération de données réalistes selon le mode de fonctionnement
    if mode == "normal":
        temp_evap = round(random.uniform(-12, -8), 1)
        temp_cond = round(random.uniform(38, 42), 1)
        press_high = round(random.uniform(11.5, 13.5), 1)
        press_low = round(random.uniform(1.8, 2.4), 1)
        superheat = round(random.uniform(7, 10), 1)
        subcooling = round(random.uniform(4, 6), 1)
        current = round(random.uniform(7.5, 8.5), 1)
        vibration = round(random.uniform(0.015, 0.030), 3)
    elif mode == "high_load":
        temp_evap = round(random.uniform(-8, -5), 1)
        temp_cond = round(random.uniform(42, 46), 1)
        press_high = round(random.uniform(13.5, 15.0), 1)
        press_low = round(random.uniform(2.2, 2.8), 1)
        superheat = round(random.uniform(6, 8), 1)
        subcooling = round(random.uniform(3, 5), 1)
        current = round(random.uniform(8.5, 10.0), 1)
        vibration = round(random.uniform(0.025, 0.040), 3)
    elif mode == "low_load":
        temp_evap = round(random.uniform(-15, -12), 1)
        temp_cond = round(random.uniform(35, 39), 1)
        press_high = round(random.uniform(10.0, 12.0), 1)
        press_low = round(random.uniform(1.5, 2.0), 1)
        superheat = round(random.uniform(8, 12), 1)
        subcooling = round(random.uniform(5, 7), 1)
        current = round(random.uniform(6.5, 7.5), 1)
        vibration = round(random.uniform(0.010, 0.025), 3)
    elif mode == "defrost":
        temp_evap = round(random.uniform(-5, 5), 1)
        temp_cond = round(random.uniform(45, 50), 1)
        press_high = round(random.uniform(14.0, 16.0), 1)
        press_low = round(random.uniform(2.5, 3.5), 1)
        superheat = round(random.uniform(3, 6), 1)
        subcooling = round(random.uniform(2, 4), 1)
        current = round(random.uniform(9.0, 11.0), 1)
        vibration = round(random.uniform(0.030, 0.050), 3)
    else:  # startup
        temp_evap = round(random.uniform(-20, -10), 1)
        temp_cond = round(random.uniform(35, 48), 1)
        press_high = round(random.uniform(10.0, 15.0), 1)
        press_low = round(random.uniform(1.2, 2.8), 1)
        superheat = round(random.uniform(5, 15), 1)
        subcooling = round(random.uniform(2, 8), 1)
        current = round(random.uniform(7.0, 10.5), 1)
        vibration = round(random.uniform(0.020, 0.045), 3)
    
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "machine_id": random.randint(1, 5),
        "operating_mode": mode,
        "temp_evaporator": temp_evap,
        "temp_condenser": temp_cond,
        "pressure_high": press_high,
        "pressure_low": press_low,
        "superheat": superheat,
        "subcooling": subcooling,
        "compressor_current": current,
        "vibration": vibration,
        # Paramètres calculés
        "temp_diff": round(temp_cond - temp_evap, 1),
        "pressure_ratio": round(press_high / press_low, 2),
        "efficiency": round(random.uniform(0.75, 0.95), 3)
    }

print("🧊 Démarrage du générateur de données pour installations frigorifiques...")
print("📡 Envoi des données vers Kafka topic 'RefrigerationStream'")

while True:
    data = generate_refrigeration_data()
    print(f"➡️ Envoi: Machine {data['machine_id']} - Mode: {data['operating_mode']} - T_evap: {data['temp_evaporator']}°C - T_cond: {data['temp_condenser']}°C")
    producer.send('RefrigerationStream', value=data)
    time.sleep(3)  # Données toutes les 3 secondes