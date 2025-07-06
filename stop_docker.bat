@echo off
echo 🛑 Arrêt du système de maintenance prédictive pour installations frigorifiques
echo 📅 %date% %time%

echo ⏹️ Arrêt des services Docker...
docker-compose down

echo 🧹 Nettoyage des ressources...
docker system prune -f

echo ✅ Système arrêté avec succès!
pause
