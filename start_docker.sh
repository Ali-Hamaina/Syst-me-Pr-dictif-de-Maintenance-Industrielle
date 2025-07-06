#!/bin/bash
# Script de démarrage pour le système de maintenance prédictive des installations frigorifiques

echo "🧊 Démarrage du système de maintenance prédictive pour installations frigorifiques"
echo "📅 $(date)"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null
then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker Desktop."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null
then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose."
    exit 1
fi

# Démarrer les services Docker
echo "🚀 Démarrage des services Docker..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier le statut des services
echo "📊 Vérification du statut des services..."
docker-compose ps

# Afficher les URLs des services
echo ""
echo "🌐 Services disponibles:"
echo "   - Dashboard principal: http://localhost:5000"
echo "   - Kafka UI: http://localhost:8080"
echo "   - MongoDB Express: http://localhost:8081 (admin/admin)"
echo ""
echo "🔧 Pour démarrer l'application Python:"
echo "   1. pip install -r requirements.txt"
echo "   2. python train_logistic.py"
echo "   3. python kafka_producer.py (dans un terminal)"
echo "   4. python streamingpredict.py (dans un autre terminal)"
echo "   5. python app.py (dans un troisième terminal)"
echo ""
echo "✅ Infrastructure Docker démarrée avec succès!"
