from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import json
from datetime import datetime
from sklearn.linear_model import LogisticRegression
import pickle
import os
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maintenance_dashboard_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for predictions and alerts
predictions = []
alerts = []

# Load the model or create a new one using LogisticRegression
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_logistic.pkl")

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ LogisticRegression model loaded successfully")
else:
    # Create a simple LogisticRegression model
    data = pd.DataFrame({
        "volt": [10.5, 11.0, 12.3, 9.8],
        "rotate": [1000, 1050, 980, 990],
        "pressure": [30.5, 32.0, 31.0, 29.8],
        "vibration": [0.02, 0.03, 0.025, 0.015],
        "status": [0, 1, 0, 1]  # 0 = OK, 1 = failure
    })
    
    X = data[["volt", "rotate", "pressure", "vibration"]]
    y = data["status"]
    
    # Train LogisticRegression model
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    
    # Save the model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print("✅ New LogisticRegression model trained and saved")

@app.route('/')
def index():
    return render_template('dashboard.html', predictions=predictions[-10:], alerts=alerts[-10:])

@app.route('/predictions')
def view_predictions():
    return render_template('predictions.html', predictions=predictions[-50:])

@app.route('/alerts')
def view_alerts():
    return render_template('alerts.html', alerts=alerts)

@app.route('/api/prediction', methods=['POST'])
def receive_prediction():
    """Receive prediction data from the streaming application"""
    try:
        data = request.json
        
        # Make prediction with LogisticRegression model
        features = np.array([[
            data['volt'],
            data['rotate'],
            data['pressure'], 
            data['vibration']
        ]])
        
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        
        # Add prediction result to the data
        data['prediction'] = prediction
        data['probability'] = probability
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Store prediction
        predictions.append(data)
        if len(predictions) > 100:  # Keep only last 100 predictions
            predictions.pop(0)
            
        # Real-time update to dashboard
        socketio.emit('new_prediction', data)
        
        # Check for alert conditions
        alerts_to_add = []
        
        # Alert condition 1: Based on prediction probability
        if prediction == 1:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚠️ Maintenance needed for machine {data['machine_id']} - Failure probability: {probability:.2%}",
                'severity': 'high' if probability > 0.75 else 'medium',
                'type': 'prediction',
                'data': data
            })
        
        # Alert condition 2: Critical voltage levels
        if data['volt'] < 9.5:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚡ Low voltage detected on machine {data['machine_id']} - Current: {data['volt']}V",
                'severity': 'high',
                'type': 'voltage',
                'data': data
            })
        elif data['volt'] > 12.5:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"⚡ High voltage detected on machine {data['machine_id']} - Current: {data['volt']}V",
                'severity': 'medium',
                'type': 'voltage',
                'data': data
            })
            
        # Alert condition 3: Abnormal vibration
        if data['vibration'] > 0.04:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📳 Excessive vibration on machine {data['machine_id']} - Current: {data['vibration']}",
                'severity': 'high',
                'type': 'vibration',
                'data': data
            })
            
        # Alert condition 4: Pressure issues
        if data['pressure'] < 28.0:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📉 Low pressure on machine {data['machine_id']} - Current: {data['pressure']} PSI",
                'severity': 'medium',
                'type': 'pressure',
                'data': data
            })
        elif data['pressure'] > 34.0:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"📈 High pressure on machine {data['machine_id']} - Current: {data['pressure']} PSI",
                'severity': 'medium',
                'type': 'pressure',
                'data': data
            })
            
        # Alert condition 5: Rotation speed issues
        if data['rotate'] < 950:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"🔄 Low rotation speed on machine {data['machine_id']} - Current: {data['rotate']} RPM",
                'severity': 'medium',
                'type': 'rotation',
                'data': data
            })
        elif data['rotate'] > 1100:
            alerts_to_add.append({
                'timestamp': data['timestamp'],
                'machine_id': data['machine_id'],
                'message': f"🔄 High rotation speed on machine {data['machine_id']} - Current: {data['rotate']} RPM",
                'severity': 'medium',
                'type': 'rotation',
                'data': data
            })
        
        # Add all generated alerts to the alerts list
        for alert in alerts_to_add:
            alerts.append(alert)
            socketio.emit('new_alert', alert)
            
        return jsonify({"status": "success", "prediction": prediction})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)