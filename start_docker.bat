@echo off
echo 🧊 Démarrage du système de maintenance prédictive pour installations frigorifiques
echo 📅 %date% %time%

REM Vérifier si Docker est installé
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker n'est pas installé. Veuillez installer Docker Desktop.
    pause
    exit /b 1
)

REM Vérifier si Docker Compose est installé
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose.
    pause
    exit /b 1
)

REM Démarrer les services Docker
echo 🚀 Démarrage des services Docker...
docker-compose up -d

REM Attendre que les services soient prêts
echo ⏳ Attente du démarrage des services...
timeout /t 30 /nobreak >nul

REM Vérifier le statut des services
echo 📊 Vérification du statut des services...
docker-compose ps

REM Afficher les URLs des services
echo.
echo 🌐 Services disponibles:
echo    - Dashboard principal: http://localhost:5000
echo    - Kafka UI: http://localhost:8080
echo    - MongoDB Express: http://localhost:8081 (admin/admin)
echo.
echo 🔧 Pour démarrer l'application Python:
echo    1. pip install -r requirements.txt
echo    2. python train_logistic.py
echo    3. python kafka_producer.py (dans un terminal)
echo    4. python streamingpredict.py (dans un autre terminal)
echo    5. python app.py (dans un troisième terminal)
echo.
echo ✅ Infrastructure Docker démarrée avec succès!
pause
