@echo off
chcp 65001 > nul
echo ==========================================
echo   Arrêt du Système de Maintenance Prédictive
echo ==========================================
echo.

echo [1/2] Arrêt des services Docker...
docker-compose down

echo.
echo [2/2] Nettoyage des ressources...
docker system prune -f

echo.
echo ✅ Tous les services ont été arrêtés avec succès!
echo.
echo Vous pouvez maintenant fermer cette fenêtre.
echo.
pause
