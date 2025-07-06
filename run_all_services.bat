@echo off
echo 🧊 Démarrage du Système de Maintenance Prédictive
echo.

echo ▶️ Démarrage de l'application Flask...
start "Flask App" python app.py

timeout /t 5 /nobreak >nul

echo ▶️ Démarrage du producteur Kafka...
start "Kafka Producer" python kafka_producer.py

timeout /t 3 /nobreak >nul

echo ▶️ Démarrage du service de prédiction...
start "Prediction Service" python streamingpredict.py

timeout /t 3 /nobreak >nul

echo.
echo ✅ Services démarrés!
echo 🌐 Dashboard: http://localhost:5001
echo 📊 Kafka UI: http://localhost:8080
echo 📈 MongoDB UI: http://localhost:8081
echo.
pause
