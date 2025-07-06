import pickle
import pandas as pd
import os
import requests
from datetime import datetime
import time
import json
from kafka import KafkaConsumer
import numpy as np

# 📦 Chargement du modèle ML pour installations frigorifiques
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_logistic_refrigeration.pkl")

# Essayer de charger le modèle spécifique aux installations frigorifiques
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ Modèle installations frigorifiques chargé avec succès")
except Exception as e:
    print(f"⚠️ Modèle frigorifique non trouvé, tentative de chargement du modèle générique...")
    try:
        # Fallback sur le modèle générique
        generic_model_path = os.path.join(BASE_DIR, "model_logistic.pkl")
        with open(generic_model_path, "rb") as f:
            model = pickle.load(f)
        print("✅ Modèle générique chargé avec succès")
    except Exception as e2:
        print(f"❌ Erreur lors du chargement du modèle : {e2}")
        print("🔧 Veuillez exécuter train_logistic.py pour créer le modèle")
        exit(1)

# Configuration Flask endpoint
FLASK_ENDPOINT = "http://localhost:5001/api/refrigeration_prediction"

# Create Kafka consumer pour les données frigorifiques
consumer = KafkaConsumer(
    'RefrigerationStream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='refrigeration-prediction-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def calculate_thermodynamic_indicators(data):
    """Calcule des indicateurs thermodynamiques supplémentaires"""
    try:
        # Coefficient de performance (COP) approximatif
        temp_evap_k = data['temp_evaporator'] + 273.15  # Conversion en Kelvin
        temp_cond_k = data['temp_condenser'] + 273.15
        theoretical_cop = temp_evap_k / (temp_cond_k - temp_evap_k)
        
        # Efficacité du compresseur
        compressor_efficiency = data.get('efficiency', 0.8)
        
        # Ratio de pression
        pressure_ratio = data['pressure_high'] / data['pressure_low']
        
        # Température de surchauffe et sous-refroidissement
        superheat_quality = "normal" if 5 <= data['superheat'] <= 12 else "abnormal"
        subcooling_quality = "normal" if 3 <= data['subcooling'] <= 8 else "abnormal"
        
        return {
            'theoretical_cop': round(theoretical_cop, 2),
            'compressor_efficiency': compressor_efficiency,
            'pressure_ratio': round(pressure_ratio, 2),
            'superheat_quality': superheat_quality,
            'subcooling_quality': subcooling_quality,
            'temp_diff': round(data['temp_condenser'] - data['temp_evaporator'], 1)
        }
    except Exception as e:
        print(f"⚠️ Erreur calcul indicateurs thermodynamiques: {e}")
        return {}

print("🧊 Démarrage du service de prédiction pour installations frigorifiques")
print("📊 Dashboard URL: http://localhost:5001")
print("🔍 Kafka UI URL: http://localhost:8080")
print("📈 MongoDB UI URL: http://localhost:8081")
print("⏳ Attente des messages depuis Kafka (RefrigerationStream)...\n")

# Traitement des messages depuis Kafka
for message in consumer:
    try:
        record = message.value
        
        # Calcul des indicateurs thermodynamiques
        thermo_indicators = calculate_thermodynamic_indicators(record)
        record.update(thermo_indicators)
        
        # Affichage des données reçues
        print(f"📡 Données reçues: Machine {record['machine_id']} - Mode: {record['operating_mode']}")
        print(f"   T_evap: {record['temp_evaporator']}°C, T_cond: {record['temp_condenser']}°C")
        print(f"   P_high: {record['pressure_high']} bar, P_low: {record['pressure_low']} bar")
        print(f"   COP théorique: {thermo_indicators.get('theoretical_cop', 'N/A')}")
        
        # Envoi vers l'API Flask
        response = requests.post(FLASK_ENDPOINT, json=record, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get('prediction', 'N/A')
            probability = result.get('probability', 0)
            status = "🟢 OK" if prediction == 0 else "🔴 ALERTE"
            print(f"✅ Prédiction: {status} (Probabilité: {probability:.1%})")
        else:
            print(f"❌ Erreur API Flask: {response.status_code} - {response.text}")
            
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Erreur traitement message: {e}")
        time.sleep(1)  # Attendre avant de continuer en cas d'erreur


