# Guide de Démarrage Rapide - Système de Maintenance Prédictive pour Installations Frigorifiques

## 🧊 Vue d'ensemble
Ce système surveille en temps réel les installations frigorifiques et prédit les défaillances potentielles en utilisant des paramètres thermodynamiques avancés.

## 🚀 Démarrage Rapide

### Option 1: Démarrage Automatique (Recommandé)
```powershell
# Exécuter le script PowerShell de configuration automatique
.\setup_and_run.ps1
```

### Option 2: Démarrage Manuel

1. **Démarrer l'infrastructure Docker**
   ```powershell
   .\start_docker.bat
   ```

2. **Installer les dépendances Python**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Entraîner les modèles ML**
   ```powershell
   python train_logistic.py
   python train_refrigeration.py
   ```

4. **Démarrer les services** (dans des terminaux séparés)
   ```powershell
   # Terminal 1: Producteur de données
   python kafka_producer.py
   
   # Terminal 2: Service de prédiction
   python streamingpredict.py
   
   # Terminal 3: Application web
   python app.py
   ```

5. **Accéder au dashboard**
   - Ouvrir http://localhost:5000 dans votre navigateur

## 🌐 Services Disponibles

| Service | URL | Utilisateur | Mot de passe |
|---------|-----|-------------|--------------|
| Dashboard Principal | http://localhost:5000 | - | - |
| Kafka UI | http://localhost:8080 | - | - |
| MongoDB Express | http://localhost:8081 | admin | admin |

## 🔧 Paramètres Surveillés

### Capteurs Principaux
- **Température Évaporateur** (-20°C à 0°C)
- **Température Condenseur** (30°C à 60°C)
- **Pression Haute** (8 à 18 bar)
- **Pression Basse** (1 à 4 bar)
- **Surchauffe** (3 à 15°C)
- **Sous-refroidissement** (2 à 10°C)
- **Courant Compresseur** (5 à 15A)
- **Vibrations** (0.01 à 0.08g)

### Indicateurs Calculés
- **COP Théorique** (Coefficient de Performance)
- **Ratio de Pression** (P_haute/P_basse)
- **Efficacité Compresseur**
- **Différence de Température** (ΔT condenseur-évaporateur)

## ⚠️ Système d'Alertes

### Alertes Critiques (Haute Priorité)
- Température évaporateur > -5°C
- Température condenseur > 50°C
- Pression haute > 16 bar
- Pression basse < 1.5 bar
- Surchauffe < 3°C (risque retour liquide)
- Courant compresseur > 12A
- Prédiction de défaillance > 75%

### Alertes Moyennes (Surveillance)
- Surchauffe > 15°C (perte efficacité)
- Vibrations > 0.05g
- Ratio de pression > 8
- Prédiction de défaillance 25-75%

## 📊 Fonctionnalités du Dashboard

### Page Principale
- **Graphiques temps réel** des paramètres thermodynamiques
- **Statut des machines** avec probabilité de défaillance
- **Alertes récentes** avec niveaux de gravité
- **Prédictions récentes** avec scores ML

### Historique des Prédictions
- Toutes les prédictions avec horodatage
- Filtrage par machine et statut
- Export des données possibles

### Gestion des Alertes
- Historique complet des alertes
- Catégorisation par type et gravité
- Détails des conditions déclenchantes

## 🛠️ Maintenance et Dépannage

### Vérification des Services
```powershell
# Statut des conteneurs Docker
docker-compose ps

# Logs des services
docker-compose logs -f kafka
docker-compose logs -f mongodb

# Statut de l'API Python
curl http://localhost:5000/api/system_status
```

### Redémarrage des Services
```powershell
# Redémarrer tous les services Docker
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart kafka
```

### Nettoyage Complet
```powershell
# Arrêter et supprimer tous les services
.\stop_docker.bat

# Ou manuellement
docker-compose down -v
docker system prune -f
```

## 📝 Modes de Fonctionnement

Le système simule différents modes de fonctionnement des installations frigorifiques:

1. **Normal** - Fonctionnement optimal
2. **Charge Élevée** - Demande frigorifique importante
3. **Charge Faible** - Demande frigorifique réduite
4. **Dégivrage** - Cycle de dégivrage automatique
5. **Démarrage** - Phase de démarrage du système

## 🔄 Workflow Typique

1. **Génération de données** par le producteur Kafka
2. **Streaming des données** vers le topic RefrigerationStream
3. **Traitement en temps réel** par le service de prédiction
4. **Analyse ML** avec calcul de la probabilité de défaillance
5. **Génération d'alertes** selon les seuils configurés
6. **Mise à jour du dashboard** en temps réel via WebSocket
7. **Stockage des données** dans MongoDB pour historique

## 🎯 Cas d'Usage

### Surveillance Continue
- Monitoring 24/7 des paramètres critiques
- Détection précoce des anomalies
- Alertes automatiques pour maintenance préventive

### Analyse des Performances
- Suivi de l'efficacité énergétique
- Optimisation des cycles de fonctionnement
- Historique des performances

### Maintenance Prédictive
- Prédiction des défaillances avant occurrence
- Planification optimale des interventions
- Réduction des coûts de maintenance

## 📈 Métriques de Performance

Le système calcule automatiquement:
- **Disponibilité** des installations
- **Efficacité énergétique** (COP)
- **Temps de fonctionnement** par mode
- **Fréquence des alertes** par type
- **Précision des prédictions** ML

## 🔧 Configuration Avancée

### Ajustement des Seuils d'Alerte
Modifier les valeurs dans `app.py`:
```python
# Exemple: Température évaporateur critique
if data['temp_evaporator'] > -5:  # Modifier cette valeur
```

### Nouveaux Paramètres de Surveillance
1. Ajouter le paramètre dans `kafka_producer.py`
2. Mettre à jour le modèle ML dans `train_logistic.py`
3. Ajouter les conditions d'alerte dans `app.py`
4. Mettre à jour l'interface dans les templates HTML

### Intégration avec Systèmes Existants
- API REST disponible pour intégration
- Format JSON standardisé
- Webhooks pour notifications externes

## 📞 Support

Pour toute question ou problème:
1. Consulter les logs: `docker-compose logs`
2. Vérifier le statut: `http://localhost:5000/api/system_status`
3. Redémarrer les services si nécessaire
4. Consulter la documentation complète dans README.md

---
**Système de Maintenance Prédictive pour Installations Frigorifiques**  
*Version 1.0 - 2024*
