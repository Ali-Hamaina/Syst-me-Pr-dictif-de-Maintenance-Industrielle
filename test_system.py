#!/usr/bin/env python3

print("🧊 Test de démarrage du système...")

try:
    print("📦 Import des modules...")
    import flask
    import flask_socketio
    import pandas
    import sklearn
    import pymongo
    import kafka
    print("✅ Tous les modules importés avec succès")
    
    print("🐳 Test de connexion MongoDB...")
    from pymongo import MongoClient
    try:
        client = MongoClient("mongodb://admin:password@localhost:27017/", serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB Docker connecté")
    except:
        try:
            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            print("✅ MongoDB local connecté")
        except Exception as e:
            print(f"⚠️ MongoDB non disponible: {e}")
    
    print("📡 Test de connexion Kafka...")
    from kafka import KafkaProducer
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: str(v).encode('utf-8'),
            request_timeout_ms=3000
        )
        print("✅ Kafka connecté")
        producer.close()
    except Exception as e:
        print(f"⚠️ Kafka non disponible: {e}")
    
    print("🤖 Test du modèle ML...")
    import pickle
    import os
    
    model_path = "model_logistic_refrigeration.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("✅ Modèle ML chargé")
    else:
        print(f"⚠️ Modèle {model_path} non trouvé")
    
    print("\n🎯 Tous les tests terminés!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
