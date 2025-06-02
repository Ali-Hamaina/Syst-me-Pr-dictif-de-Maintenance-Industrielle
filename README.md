# Predictive Maintenance Dashboard

This project implements a real-time predictive maintenance system using Apache Kafka for data streaming, Machine Learning for failure prediction, and a Flask web application for visualization.

## Project Overview

The Predictive Maintenance Dashboard monitors machine health metrics in real-time and predicts potential failures before they occur. The system collects sensor data (voltage, rotation, pressure, vibration) from machines, processes this data through a machine learning model, and displays predictions and alerts on a web dashboard.

### Key Features

- **Real-time Data Streaming**: Using Apache Kafka to ingest and process sensor data
- **Machine Learning Predictions**: Logistic Regression model to predict machine failures
- **Interactive Dashboard**: Real-time visualization of machine status and sensor readings
- **Alert System**: Notification system for potential machine failures
- **WebSocket Integration**: Live updates to the dashboard without page refresh

## Technology Stack

- **Backend**: Flask, Flask-SocketIO
- **Data Processing**: Apache Kafka, PySpark
- **Machine Learning**: scikit-learn (Logistic Regression)
- **Frontend**: Bootstrap 5, Chart.js, Socket.IO
- **Database**: MongoDB
- **Other Tools**: Python, pandas, NumPy

## Project Structure

```
├── app.py                  # Main Flask application
├── kafka_consumer.py       # Kafka consumer for reading data stream
├── kafka_producer.py       # Kafka producer for generating sample data
├── streamingpredict.py     # Real-time prediction service
├── train_logistic.py       # Script to train logistic regression model
├── model_logistic.pkl      # Trained machine learning model
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── dashboard.html      # Main dashboard UI
│   ├── alerts.html         # Alerts history page
│   └── predictions.html    # Predictions history page
└── static/                 # Static assets (CSS, JS, images)
```

## Setup and Installation

### Prerequisites

- Python 3.7+
- Apache Kafka
- MongoDB
- Git

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository_url>
   cd bigdata
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure Kafka is running:
   Make sure Kafka and Zookeeper services are running on your machine.
   ```
   # Typically on Windows:
   # Start Zookeeper
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
   
   # Start Kafka
   .\bin\windows\kafka-server-start.bat .\config\server.properties
   ```

5. Ensure MongoDB is running:
   ```
   # Check MongoDB connection
   python check_mongo.py
   ```

## Running the Application

1. Start the Kafka producer in a terminal to generate sample data:
   ```
   python kafka_producer.py
   ```

2. Start the Kafka consumer in another terminal to monitor incoming messages (optional but helpful for debugging):
   ```
   python kafka_consumer.py
   ```

3. Start the streaming prediction service in another terminal:
   ```
   python streamingpredict.py
   ```

4. Start the Flask web application in another terminal:
   ```
   python app.py
   ```

5. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Using the Dashboard

1. The main dashboard displays:
   - Machine status overview chart
   - Live sensor readings (voltage, rotation, pressure, vibration)
   - Recent alerts with severity indicators
   - Recent predictions with probability scores

2. Navigate to the "Predictions History" page to see all past predictions.

3. Navigate to the "Alerts" page to see all alerts and their details.

## Training the Model

To retrain the machine learning model with new data:

```
python train_logistic.py
```

This will generate a new model file `model_logistic.pkl` that will be used by the application.

## Troubleshooting

- If the Kafka connection fails, ensure Kafka and Zookeeper services are running correctly.
- If the dashboard doesn't update in real-time, check if WebSocket connections are being established.
- For MongoDB connection issues, verify your MongoDB service is running and accessible.

---

Created by [Your Name/Team] - June 2025
