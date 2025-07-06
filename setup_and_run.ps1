# Script PowerShell pour démarrer le système de maintenance prédictive des installations frigorifiques

Write-Host "🧊 Système de Maintenance Prédictive pour Installations Frigorifiques" -ForegroundColor Cyan
Write-Host "📅 $(Get-Date)" -ForegroundColor Gray

# Fonction pour vérifier si une commande existe
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Vérifier Docker
if (-not (Test-Command "docker")) {
    Write-Host "❌ Docker n'est pas installé. Veuillez installer Docker Desktop." -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Vérifier Docker Compose
if (-not (Test-Command "docker-compose")) {
    Write-Host "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose." -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Vérifier Python
if (-not (Test-Command "python")) {
    Write-Host "❌ Python n'est pas installé. Veuillez installer Python 3.8+." -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

Write-Host "✅ Prérequis vérifiés avec succès" -ForegroundColor Green

# Installer les dépendances Python
Write-Host "📦 Installation des dépendances Python..." -ForegroundColor Yellow
pip install -r requirements.txt

# Démarrer les services Docker
Write-Host "🚀 Démarrage des services Docker..." -ForegroundColor Yellow
docker-compose up -d

# Attendre que les services soient prêts
Write-Host "⏳ Attente du démarrage des services (30 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Vérifier le statut des services
Write-Host "📊 Vérification du statut des services..." -ForegroundColor Yellow
docker-compose ps

# Entraîner le modèle ML
Write-Host "🤖 Entraînement du modèle de Machine Learning..." -ForegroundColor Yellow
python train_logistic.py

# Afficher les informations de démarrage
Write-Host ""
Write-Host "🌐 Services disponibles:" -ForegroundColor Green
Write-Host "   - Dashboard principal: http://localhost:5000" -ForegroundColor Cyan
Write-Host "   - Kafka UI: http://localhost:8080" -ForegroundColor Cyan
Write-Host "   - MongoDB Express: http://localhost:8081 (admin/admin)" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Pour démarrer l'application complète:" -ForegroundColor Green
Write-Host "   1. Ouvrir un terminal et exécuter: python kafka_producer.py" -ForegroundColor White
Write-Host "   2. Ouvrir un autre terminal et exécuter: python streamingpredict.py" -ForegroundColor White
Write-Host "   3. Ouvrir un troisième terminal et exécuter: python app.py" -ForegroundColor White
Write-Host "   4. Ouvrir http://localhost:5000 dans votre navigateur" -ForegroundColor White
Write-Host ""

# Demander si l'utilisateur veut démarrer automatiquement
$choice = Read-Host "Voulez-vous démarrer automatiquement l'application? (y/n)"
if ($choice -eq 'y' -or $choice -eq 'Y') {
    Write-Host "🚀 Démarrage automatique de l'application..." -ForegroundColor Green
    
    # Démarrer le producteur Kafka en arrière-plan
    Write-Host "▶️ Démarrage du producteur Kafka..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python kafka_producer.py"
    Start-Sleep -Seconds 3
    
    # Démarrer le service de prédiction en arrière-plan
    Write-Host "▶️ Démarrage du service de prédiction..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python streamingpredict.py"
    Start-Sleep -Seconds 3
    
    # Démarrer l'application Flask
    Write-Host "▶️ Démarrage de l'application Flask..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python app.py"
    Start-Sleep -Seconds 5
    
    # Ouvrir le navigateur
    Write-Host "🌐 Ouverture du navigateur..." -ForegroundColor Yellow
    Start-Process "http://localhost:5000"
}

Write-Host ""
Write-Host "✅ Système démarré avec succès!" -ForegroundColor Green
Write-Host "📝 Consultez le README.md pour plus d'informations" -ForegroundColor Gray
Read-Host "Appuyez sur Entrée pour quitter"
