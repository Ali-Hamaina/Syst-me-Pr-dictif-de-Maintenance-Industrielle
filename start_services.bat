@echo off
echo 🧊 Démarrage du système de maintenance prédictive
echo.

echo ▶️ Démarrage du service de prédiction...
start "Streaming Prediction" cmd /k "python streamingpredict.py"
timeout /t 3 /nobreak >nul

echo ▶️ Démarrage de l'application Flask...
start "Flask App" cmd /k "python app.py"
timeout /t 5 /nobreak >nul

echo.
echo ✅ Services démarrés!
echo 🌐 Dashboard: http://localhost:5001
echo 🔍 Kafka UI: http://localhost:8080
echo 📈 MongoDB UI: http://localhost:8081
pause
