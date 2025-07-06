from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import json
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'refrigeration_maintenance_dashboard_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration MongoDB
try:
    # Try to connect to MongoDB (Docker or local)
    try:
        # First try with Docker MongoDB (with auth)
        client = MongoClient("mongodb://admin:password@localhost:27017/")
        client.admin.command('ping')  # Test connection
        db = client["refrigeration_maintenance"]
    except:
        # Fallback to local MongoDB (without auth)
        client = MongoClient("mongodb://localhost:27017/")
        client.admin.command('ping')  # Test connection
        db = client["refrigeration_maintenance"]
    
    predictions_collection = db["predictions"]
    alerts_collection = db["alerts"]
    sensors_collection = db["sensors_data"]
    logger.info("✅ Connexion MongoDB établie")
except Exception as e:
    logger.warning(f"⚠️ MongoDB non disponible: {e}")
    logger.info("📝 Utilisation du stockage en mémoire")
    # Fallback sur stockage en mémoire
    predictions_collection = None
    alerts_collection = None
    sensors_collection = None

# Stockage en mémoire comme backup
predictions = []
alerts = []
sensors_data = []

# Chargement du modèle pour installations frigorifiques
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_logistic_refrigeration.pkl")

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    logger.info("✅ Modèle installations frigorifiques chargé avec succès")
else:
    # Créer un modèle pour installations frigorifiques
    logger.info("🔧 Création d'un nouveau modèle pour installations frigorifiques...")
    data = pd.DataFrame({
        "temp_evaporator": [-10.5, -8.0, -12.3, -15.8, -7.2, -11.0, -9.5, -13.1],
        "temp_condenser": [40.5, 38.0, 45.3, 42.8, 39.2, 44.0, 41.5, 46.1],
        "pressure_high": [12.5, 11.8, 14.2, 13.1, 12.0, 13.8, 12.7, 14.5],
        "pressure_low": [2.1, 2.3, 1.8, 1.9, 2.4, 1.7, 2.2, 1.6],
        "superheat": [8.5, 9.2, 7.8, 6.9, 9.8, 7.2, 8.9, 6.5],
        "subcooling": [5.2, 4.8, 6.1, 5.7, 4.5, 6.3, 5.0, 6.8],
        "compressor_current": [8.2, 7.9, 9.5, 8.8, 7.6, 9.2, 8.5, 9.8],
        "vibration": [0.02, 0.03, 0.025, 0.015, 0.035, 0.018, 0.028, 0.042],
        "status": [0, 0, 1, 1, 0, 1, 0, 1]
    })
    
    X = data[["temp_evaporator", "temp_condenser", "pressure_high", "pressure_low", 
              "superheat", "subcooling", "compressor_current", "vibration"]]
    y = data["status"]
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, y)
    
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    logger.info("✅ Nouveau modèle installations frigorifiques créé et sauvegardé")

def get_predictions_from_db(limit=50):
    """Récupère les prédictions depuis MongoDB ou mémoire"""
    if predictions_collection is not None:
        try:
            return list(predictions_collection.find().sort("timestamp", -1).limit(limit))
        except:
            pass
    return predictions[-limit:] if predictions else []

def get_alerts_from_db(limit=50):
    """Récupère les alertes depuis MongoDB ou mémoire"""
    if alerts_collection is not None:
        try:
            return list(alerts_collection.find().sort("timestamp", -1).limit(limit))
        except:
            pass
    return alerts[-limit:] if alerts else []

@app.route('/')
def index():
    recent_predictions = get_predictions_from_db(10)
    recent_alerts = get_alerts_from_db(10)
    return render_template('dashboard.html', 
                         predictions=recent_predictions, 
                         alerts=recent_alerts)

@app.route('/predictions')
def view_predictions():
    all_predictions = get_predictions_from_db(100)
    return render_template('predictions.html', predictions=all_predictions)

@app.route('/alerts')
def view_alerts():
    all_alerts = get_alerts_from_db(100)
    return render_template('alerts.html', alerts=all_alerts)

@app.route('/api/refrigeration_prediction', methods=['POST'])
def receive_refrigeration_prediction():
    """Reçoit les données de prédiction pour installations frigorifiques"""
    try:
        data = request.json
        
        # Prédiction avec le modèle installations frigorifiques
        features = np.array([[
            data['temp_evaporator'],
            data['temp_condenser'],
            data['pressure_high'],
            data['pressure_low'],
            data['superheat'],
            data['subcooling'],
            data['compressor_current'],
            data['vibration']
        ]])
        
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        
        # Ajout des résultats de prédiction
        data['prediction'] = prediction
        data['probability'] = probability
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Stockage dans MongoDB
        if predictions_collection is not None:
            try:
                predictions_collection.insert_one(data.copy())
            except Exception as e:
                logger.error(f"Erreur insertion MongoDB: {e}")
        
        # Stockage en mémoire
        predictions.append(data)
        if len(predictions) > 200:
            predictions.pop(0)
        
        # Stockage des données capteurs
        if sensors_collection is not None:
            try:
                sensors_collection.insert_one(data.copy())
            except:
                pass
        
        # Mise à jour temps réel dashboard
        socketio.emit('new_prediction', data)
        
        # Vérification des conditions d'alerte spécifiques aux installations frigorifiques
        alerts_to_add = []
        
        # Alerte 1: Prédiction de défaillance
        if prediction == 1:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚠️ Maintenance préventive requise - Installation frigorifique {data['machine_id']} - Probabilité: {probability:.1%}",
                'severity': 'high' if probability > 0.75 else 'medium',
                'type': 'prediction',
                'data': data
            })
        
        # Alerte 2: Températures critiques
        if data['temp_evaporator'] > -5:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"🌡️ Température évaporateur élevée: {data['temp_evaporator']}°C - Risque de perte de capacité frigorifique",
                'severity': 'high',
                'type': 'temperature',
                'data': data
            })
        
        if data['temp_condenser'] > 50:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"🌡️ Température condenseur critique: {data['temp_condenser']}°C - Risque de surchauffe",
                'severity': 'high',
                'type': 'temperature',
                'data': data
            })
        
        # Alerte 3: Pressions anormales
        if data['pressure_high'] > 16:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📈 Pression haute critique: {data['pressure_high']} bar - Risque de déclenchement des sécurités",
                'severity': 'high',
                'type': 'pressure',
                'data': data
            })
        
        if data['pressure_low'] < 1.5:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📉 Pression basse critique: {data['pressure_low']} bar - Risque de perte de fluide frigorigène",
                'severity': 'high',
                'type': 'pressure',
                'data': data
            })
        
        # Alerte 4: Surchauffe et sous-refroidissement
        if data['superheat'] < 3:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"❄️ Surchauffe faible: {data['superheat']}°C - Risque de retour liquide compresseur",
                'severity': 'high',
                'type': 'superheat',
                'data': data
            })
        
        if data['superheat'] > 15:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"🔥 Surchauffe excessive: {data['superheat']}°C - Perte d'efficacité énergétique",
                'severity': 'medium',
                'type': 'superheat',
                'data': data
            })
        
        # Alerte 5: Courant compresseur
        if data['compressor_current'] > 12:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚡ Courant compresseur élevé: {data['compressor_current']}A - Surcharge détectée",
                'severity': 'high',
                'type': 'current',
                'data': data
            })
        
        # Alerte 6: Vibrations
        if data['vibration'] > 0.05:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📳 Vibrations excessives: {data['vibration']}g - Vérifier fixations et paliers",
                'severity': 'medium',
                'type': 'vibration',
                'data': data
            })
        
        # Alerte 7: Ratio de pression
        pressure_ratio = data['pressure_high'] / data['pressure_low']
        if pressure_ratio > 8:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚖️ Ratio de pression élevé: {pressure_ratio:.1f} - Efficacité réduite",
                'severity': 'medium',
                'type': 'pressure_ratio',
                'data': data
            })
        
        # Traitement des alertes
        for alert in alerts_to_add:
            # Stockage MongoDB
            if alerts_collection is not None:
                try:
                    alerts_collection.insert_one(alert.copy())
                except Exception as e:
                    logger.error(f"Erreur insertion alerte MongoDB: {e}")
            
            # Stockage mémoire
            alerts.append(alert)
            if len(alerts) > 100:
                alerts.pop(0)
            
            # Émission temps réel
            socketio.emit('new_alert', alert)
        
        return jsonify({
            "status": "success", 
            "prediction": prediction,
            "probability": probability,
            "alerts_generated": len(alerts_to_add)
        })
        
    except Exception as e:
        logger.error(f"Erreur traitement prédiction: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/system_status')
def system_status():
    """Retourne le statut du système"""
    return jsonify({
        "status": "running",
        "model_loaded": MODEL_PATH,
        "mongodb_connected": predictions_collection is not None,
        "predictions_count": len(predictions),
        "alerts_count": len(alerts)
    })

if __name__ == '__main__':
    # Création des dossiers nécessaires
    os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
    
    logger.info("🧊 Démarrage dashboard maintenance prédictive installations frigorifiques")
    logger.info("🌐 http://localhost:5001")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)