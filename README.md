# 🧊 Système de Maintenance Prédictive pour Installations Frigorifiques

> **Un système intelligent de surveillance et de prédiction des défaillances pour les installations frigorifiques et thermodynamiques**

Ce projet implémente un système de maintenance prédictive en temps réel pour les installations frigorifiques utilisant Apache Kafka pour le streaming de données, Machine Learning pour la prédiction des défaillances, et une interface web Flask pour la visualisation et l'analyse thermodynamique.

## 🌟 Fonctionnalités clés

✅ **Surveillance en temps réel** - Monitoring continu des paramètres thermodynamiques  
✅ **Prédiction IA** - Modèles ML pour anticiper les défaillances  
✅ **Interface moderne** - Dashboard interactif avec mises à jour en temps réel  
✅ **Alertes intelligentes** - Notifications automatiques basées sur les seuils critiques  
✅ **Containerisation** - Déploiement facile avec Docker Compose  
✅ **Architecture scalable** - Kafka pour le streaming haute performance  
✅ **Analyse thermodynamique** - Calculs automatiques des indicateurs de performance  

## 🎯 Vue d'ensemble du projet

Le système surveille en temps réel les paramètres critiques des installations frigorifiques (températures, pressions, surchauffe, sous-refroidissement, consommation électrique, vibrations) et utilise des algorithmes d'apprentissage automatique pour prédire les défaillances avant qu'elles ne se produisent.

**Avantages** :
- 🔍 **Détection précoce** des anomalies
- 💰 **Réduction des coûts** de maintenance
- ⚡ **Optimisation énergétique** des installations
- 📊 **Analyse des tendances** et historiques
- 🔧 **Maintenance proactive** au lieu de corrective

## 📸 Aperçu du tableau de bord

### Dashboard Principal
![Dashboard Principal](./screenshots/dashboard-main.svg)
*Vue d'ensemble du tableau de bord avec monitoring temps réel*

### Alertes et Notifications
![Alertes](./screenshots/alerts-page.svg)
*Page des alertes avec historique des événements*

### Prédictions ML
![Prédictions](./screenshots/predictions-page.svg)
*Historique des prédictions avec scores de confiance*

> 📝 **Note** : Les images ci-dessus sont des exemples visuels. Pour voir le vrai tableau de bord, démarrez l'application avec `.\run_all_services.bat` et allez sur http://localhost:5001
> 
> 🔄 **Mise à jour** : Pour remplacer ces exemples par de vraies captures d'écran, suivez les instructions dans le dossier `screenshots/`

### Fonctionnalités principales

- **Streaming de données en temps réel** : Utilisation d'Apache Kafka pour ingérer et traiter les données de capteurs
- **Prédictions Machine Learning** : Modèle de régression logistique pour prédire les défaillances d'installations frigorifiques
- **Analyse thermodynamique** : Calcul automatique des indicateurs de performance (COP, ratio de pression, etc.)
- **Tableau de bord interactif** : Visualisation en temps réel des statuts des machines et des lectures de capteurs
- **Système d'alertes** : Notifications automatiques pour les défaillances potentielles et conditions anormales
- **Intégration WebSocket** : Mises à jour en direct du tableau de bord sans actualisation de page
- **Containerisation Docker** : Déploiement facile avec Docker Compose

## 🛠️ Technologies utilisées

### Backend & Services
- **Flask** + **Flask-SocketIO** - Framework web Python avec WebSocket
- **Apache Kafka** - Streaming de données en temps réel
- **MongoDB** - Base de données NoSQL pour stockage
- **Docker** + **Docker Compose** - Containerisation et orchestration

### Machine Learning & Données
- **scikit-learn** - Algorithmes ML (Régression logistique, Random Forest)
- **pandas** + **NumPy** - Manipulation et analyse des données
- **PySpark** - Traitement distribué des données (optionnel)

### Frontend & Interface
- **Bootstrap 5** - Framework CSS moderne et responsive
- **Chart.js** - Graphiques interactifs et animations
- **Socket.IO** - Communication bidirectionnelle en temps réel
- **HTML5** + **CSS3** + **JavaScript ES6+**

### Outils de développement
- **Python 3.8+** - Langage principal
- **Git** - Contrôle de version
- **VS Code** - IDE recommandé

## 🏗️ Architecture du système

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Capteurs IoT  │───▶│  Kafka Producer │───▶│  Kafka Broker   │
│  (Simulation)   │    │  (Génération)   │    │  (Streaming)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │◀───│  Flask WebApp   │◀───│ Streaming ML    │
│  (Interface)    │    │  (API + UI)     │    │  (Prédictions)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │    MongoDB      │    │   Modèles ML    │
                       │  (Stockage)     │    │ (Entraînement)  │
                       └─────────────────┘    └─────────────────┘
```

## 📁 Structure du projet

```
📦 Syst-me-Pr-dictif-de-Maintenance-Industrielle/
├── 🐍 **Scripts Python**
│   ├── app.py                          # 🌐 Application Flask principale
│   ├── kafka_consumer.py               # 📥 Consommateur Kafka
│   ├── kafka_producer.py               # 📤 Producteur Kafka (simulation)
│   ├── streamingpredict.py             # 🔮 Service de prédiction temps réel
│   ├── train_refrigeration.py          # 🧠 Entraînement Random Forest
│   ├── train_logistic.py               # 🧠 Entraînement Régression Logistique
│   ├── check_mongo.py                  # 🔍 Test connectivité MongoDB
│   └── test_system.py                  # 🧪 Test système complet
├── 🤖 **Modèles ML**
│   ├── model_logistic_refrigeration.pkl # 📊 Modèle de prédiction
│   └── model.pkl                       # 📊 Modèle alternatif
├── 🌐 **Interface Web**
│   └── templates/
│       ├── dashboard.html              # 🏠 Tableau de bord principal
│       ├── alerts.html                 # 🚨 Historique des alertes
│       └── predictions.html            # 📈 Historique des prédictions
├── 🐳 **Configuration Docker**
│   ├── docker-compose.yml              # 🐋 Orchestration des services
│   └── mongo-init.js                   # 🗄️ Initialisation MongoDB
├── 🔧 **Scripts d'automatisation**
│   ├── run_all_services.bat            # ▶️ Démarrage automatique
│   └── stop_all_services.bat           # ⏹️ Arrêt des services
├── 📋 **Configuration**
│   ├── requirements.txt                # 📦 Dépendances Python
│   └── README.md                       # 📖 Documentation
├── 📸 **Documentation**
│   └── screenshots/                    # 🖼️ Captures d'écran du dashboard
│       ├── dashboard-main.svg          # 🏠 Tableau de bord principal (exemple)
│       ├── alerts-page.svg             # 🚨 Page des alertes (exemple)
│       ├── predictions-page.svg        # 📈 Page des prédictions (exemple)
│       └── README.md                   # 📝 Instructions pour les captures
└── 🗂️ **Ressources**
    └── static/                         # 🎨 CSS, JS, Images
```

## 🚀 Démarrage rapide

### Option 1 : Utilisation du script automatique (Recommandé)

1. **Ouvrir PowerShell en tant qu'administrateur** dans le dossier du projet
2. **Exécuter le script de démarrage** :
   ```powershell
   .\run_all_services.bat
   ```
3. **Attendre que tous les services se lancent** (environ 2-3 minutes)
4. **Ouvrir votre navigateur** et aller sur : `http://localhost:5001`

### Option 2 : Démarrage manuel (étape par étape)

Si vous préférez comprendre chaque étape, suivez les instructions détaillées ci-dessous.

## 📋 Installation et configuration

### Prérequis

- **Python 3.8+** : [Télécharger Python](https://www.python.org/downloads/)
- **Docker Desktop** : [Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Git** : [Télécharger Git](https://git-scm.com/downloads)
- **8 Go de RAM** recommandés pour une performance optimale

### Étapes d'installation détaillées

#### 1. Cloner le dépôt
```powershell
git clone <repository_url>
cd Syst-me-Pr-dictif-de-Maintenance-Industrielle
```

#### 2. Créer et activer un environnement virtuel Python
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate

# Vérifier que l'environnement est activé (vous devriez voir (venv) dans le prompt)
```

#### 3. Installer les dépendances Python
```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

#### 4. Vérifier l'installation de Docker
```powershell
# Vérifier que Docker est installé et en cours d'exécution
docker --version
docker-compose --version

# Démarrer Docker Desktop si ce n'est pas déjà fait
```

#### 5. Démarrer l'infrastructure Docker
```powershell
# Démarrer tous les services Docker en arrière-plan
docker-compose up -d

# Vérifier que les services sont démarrés
docker-compose ps
```

Les services suivants seront démarrés :
- **Zookeeper** (port 2181) : Service de coordination pour Kafka
- **Kafka** (port 9092) : Plateforme de streaming distribué
- **MongoDB** (port 27017) : Base de données NoSQL
- **Kafka UI** (port 8080) : Interface web pour Kafka
- **Mongo Express** (port 8081) : Interface web pour MongoDB

#### 6. Vérifier que les services sont opérationnels
```powershell
# Tester la connectivité du système
python test_system.py
```

Vous pouvez aussi vérifier manuellement :
- **Kafka UI** : http://localhost:8080
- **MongoDB Express** : http://localhost:8081 (utilisateur : admin, mot de passe : admin)
- **MongoDB** : Connexion sur `mongodb://localhost:27017`

#### 7. Entraîner le modèle de Machine Learning
```powershell
# Entraîner le modèle de régression logistique pour la maintenance prédictive
python train_logistic.py

# Vérifier que le modèle a été créé
ls model_logistic_refrigeration.pkl
```

## 🎯 Utilisation de l'application

### Démarrage du système complet

Une fois l'installation terminée, vous avez deux options pour démarrer l'application :

#### Option A : Démarrage automatique (recommandé)
```powershell
# Exécuter le script qui démarre tous les services
.\run_all_services.bat
```
Ce script va automatiquement :
1. Démarrer le producteur Kafka (génération de données)
2. Démarrer le service de prédiction en streaming
3. Démarrer l'application web Flask

#### Option B : Démarrage manuel (pour le développement)

Si vous voulez contrôler chaque service individuellement :

1. **Démarrer le producteur Kafka** dans un premier terminal :
   ```powershell
   python kafka_producer.py
   ```

2. **Démarrer le service de prédiction en streaming** dans un deuxième terminal :
   ```powershell
   python streamingpredict.py
   ```

3. **Démarrer l'application web Flask** dans un troisième terminal :
   ```powershell
   python app.py
   ```

4. **Optionnel - Surveiller les messages Kafka** dans un quatrième terminal :
   ```powershell
   python kafka_consumer.py
   ```

### Accès au tableau de bord

Une fois tous les services démarrés, ouvrez votre navigateur web et allez sur :
```
http://localhost:5001
```

> **Note importante** : Le port a été changé de 5000 à 5001 pour éviter les conflits avec les services système de Windows.

### Interfaces disponibles

- **Tableau de bord principal** : http://localhost:5001
- **Kafka UI** : http://localhost:8080 (surveillance des messages)
- **MongoDB Express** : http://localhost:8081 (consultation de la base de données)
  - Utilisateur : `admin`
  - Mot de passe : `admin`

### Arrêt du système

Pour arrêter proprement tous les services :

```powershell
# Arrêter les services Python (Ctrl+C dans chaque terminal)
# Puis arrêter les services Docker
docker-compose down
```

Ou utilisez le script d'arrêt :
```powershell
.\stop_all_services.bat
```

### Utilisation du tableau de bord

1. **Tableau de bord principal** affiche :
   - Graphique de vue d'ensemble du statut des machines
   - Lectures de capteurs en temps réel (températures, pressions, surchauffe, sous-refroidissement)
   - Alertes récentes avec indicateurs de gravité
   - Prédictions récentes avec scores de probabilité

2. **Navigation vers la page "Historique des prédictions"** pour voir toutes les prédictions passées.

3. **Navigation vers la page "Alertes"** pour voir toutes les alertes et leurs détails.

## Paramètres surveillés

### Capteurs thermodynamiques
- **Température évaporateur** : Température de vaporisation du fluide frigorigène
- **Température condenseur** : Température de condensation du fluide frigorigène
- **Pression haute** : Pression côté refoulement du compresseur
- **Pression basse** : Pression côté aspiration du compresseur
- **Surchauffe** : Différence entre température gaz aspiré et température d'évaporation
- **Sous-refroidissement** : Différence entre température de condensation et température liquide
- **Courant compresseur** : Consommation électrique du compresseur
- **Vibrations** : Niveau de vibrations mécaniques

### Indicateurs calculés
- **COP théorique** : Coefficient de performance théorique
- **Ratio de pression** : Rapport entre pression haute et basse
- **Efficacité compresseur** : Efficacité énergétique du compresseur
- **Différence de température** : Écart entre températures condenseur et évaporateur

## Système d'alertes

Le système génère automatiquement des alertes basées sur :

1. **Prédictions de défaillance** : Alertes haute/moyenne priorité selon la probabilité
2. **Températures critiques** : Évaporateur > -5°C, Condenseur > 50°C
3. **Pressions anormales** : Haute > 16 bar, Basse < 1.5 bar
4. **Surchauffe inadéquate** : < 3°C (risque retour liquide) ou > 15°C (perte efficacité)
5. **Courant compresseur élevé** : > 12A (surcharge)
6. **Vibrations excessives** : > 0.05g (problème mécanique)
7. **Ratio de pression élevé** : > 8 (efficacité réduite)

## Entraînement du modèle

Pour réentraîner le modèle d'apprentissage automatique avec de nouvelles données :

```powershell
# Modèle de régression logistique
python train_logistic.py

# Modèle Random Forest
python train_refrigeration.py
```

Ces scripts génèrent de nouveaux fichiers de modèles qui seront utilisés par l'application.

## Configuration Docker

### Services inclus

- **Zookeeper** : Service de coordination pour Kafka
- **Kafka** : Plateforme de streaming distribué
- **Kafka UI** : Interface web pour Kafka (port 8080)
- **MongoDB** : Base de données NoSQL pour le stockage des données
- **Mongo Express** : Interface web pour MongoDB (port 8081)

### Commandes Docker utiles

```powershell
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Voir les logs
docker-compose logs -f

# Redémarrer un service spécifique
docker-compose restart kafka

# Supprimer tous les volumes (réinitialisation complète)
docker-compose down -v
```

## 🔧 Dépannage

### Problèmes courants et solutions

#### 1. **Échec de connexion Kafka**
**Symptôme** : `kafka.errors.NoBrokersAvailable`
**Solutions** :
```powershell
# Vérifier que les services Docker sont démarrés
docker-compose ps

# Vérifier les logs Kafka
docker-compose logs kafka

# Redémarrer Kafka si nécessaire
docker-compose restart kafka
```

#### 2. **Port 5000 déjà utilisé**
**Symptôme** : `OSError: [WinError 10048] Only one usage of each socket address`
**Solution** : L'application utilise maintenant le port 5001 par défaut
```powershell
# Accédez au tableau de bord sur le nouveau port
http://localhost:5001
```

#### 3. **Problèmes de connexion MongoDB**
**Symptôme** : `ServerSelectionTimeoutError`
**Solutions** :
```powershell
# Vérifier que MongoDB est en cours d'exécution
docker-compose ps | findstr mongo

# Tester la connexion MongoDB
python check_mongo.py

# Redémarrer MongoDB
docker-compose restart mongodb
```

#### 4. **Erreurs de modèle ML**
**Symptôme** : `FileNotFoundError: model_logistic_refrigeration.pkl`
**Solutions** :
```powershell
# Entraîner le modèle
python train_logistic.py

# Vérifier la présence du fichier
dir *.pkl
```

#### 5. **Le tableau de bord ne se met pas à jour**
**Symptôme** : Les données ne s'affichent pas en temps réel
**Solutions** :
```powershell
# Vérifier que streamingpredict.py est en cours d'exécution
# Vérifier que kafka_producer.py génère des données
# Vérifier les connexions WebSocket dans la console du navigateur (F12)
```

#### 6. **Problèmes spécifiques à Windows**

**Erreur d'encodage dans les scripts batch** :
```powershell
# Si vous rencontrez des problèmes avec les caractères spéciaux
# Utilisez PowerShell au lieu de CMD
# Ou définissez l'encodage UTF-8
chcp 65001
```

**Problèmes avec les permissions Docker** :
```powershell
# Exécuter PowerShell en tant qu'administrateur
# Ou ajouter votre utilisateur au groupe docker-users
```

**Conflits de port avec les services Windows** :
```powershell
# Vérifier quels ports sont utilisés
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :9092
```

### Diagnostic automatique

Utilisez le script de test système pour diagnostiquer les problèmes :
```powershell
python test_system.py
```

Ce script vérifie :
- ✅ Installation de Python et des dépendances
- ✅ Connectivité Docker
- ✅ Connectivité Kafka
- ✅ Connectivité MongoDB
- ✅ Présence des modèles ML
- ✅ Connectivité des services web

### Surveillance des performances

- **Kafka UI** : http://localhost:8080 - Surveiller les topics et messages
- **MongoDB Express** : http://localhost:8081 - Consulter les données stockées
- **API système** : http://localhost:5001/api/system_status - Statut de l'API

### Commandes Docker utiles

```powershell
# Voir l'état de tous les services
docker-compose ps

# Voir les logs en temps réel
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f kafka

# Redémarrer un service spécifique
docker-compose restart kafka

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer tous les volumes (réinitialisation complète)
docker-compose down -v

# Reconstruire les images Docker
docker-compose build --no-cache

# Nettoyer les ressources Docker inutilisées
docker system prune -a
```

### Réinitialisation complète

Si vous rencontrez des problèmes persistants :

```powershell
# 1. Arrêter tous les services
docker-compose down -v

# 2. Nettoyer Docker
docker system prune -a

# 3. Supprimer les modèles ML
Remove-Item *.pkl

# 4. Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# 5. Redémarrer tout
docker-compose up -d
python train_logistic.py
.\run_all_services.bat
```

## 🚀 Développement et contribution

### Structure des données

Les données de capteurs suivent ce format JSON :
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "machine_id": 1,
  "operating_mode": "normal",
  "temp_evaporator": -10.5,
  "temp_condenser": 40.5,
  "pressure_high": 12.5,
  "pressure_low": 2.1,
  "superheat": 8.5,
  "subcooling": 5.2,
  "compressor_current": 8.2,
  "vibration": 0.020,
  "efficiency": 0.85
}
```

### Ajout de nouvelles fonctionnalités

1. **Nouveaux capteurs** : Modifier `kafka_producer.py` et `app.py`
2. **Nouvelles alertes** : Ajouter des conditions dans `receive_refrigeration_prediction()`
3. **Nouvelles visualisations** : Modifier les templates HTML et ajouter des graphiques Chart.js
4. **Nouveaux modèles ML** : Créer de nouveaux scripts d'entraînement basés sur `train_logistic.py`

### Améliorations futures

- 🔌 **Intégration IoT** : Connexion avec de vrais capteurs via MQTT
- 📊 **Modèles avancés** : Deep Learning avec TensorFlow/PyTorch
- 🌍 **Multi-sites** : Surveillance de plusieurs installations
- 📱 **Application mobile** : Interface native Android/iOS
- 🔐 **Authentification** : Système de connexion utilisateur
- 📈 **Analytics avancés** : Tableaux de bord personnalisés
- 🌐 **API REST** : Interface pour intégrations tierces
- 📧 **Notifications** : Alertes par email/SMS

### Guide de contribution

1. **Fork** le projet
2. **Créer une branche** pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commiter** vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Pusher** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer une Pull Request**

### 📸 Mise à jour des captures d'écran

Pour ajouter ou mettre à jour les captures d'écran du tableau de bord :

```powershell
# 1. Démarrer l'application
.\run_all_services.bat

# 2. Attendre que les services soient prêts (2-3 minutes)
# 3. Ouvrir http://localhost:5001 dans votre navigateur
# 4. Prendre des captures d'écran de :
#    - Dashboard principal (page d'accueil)
#    - Page des alertes (/alerts)
#    - Page des prédictions (/predictions)
# 5. Sauvegarder les images dans le dossier screenshots/
# 6. Mettre à jour les liens dans le README si nécessaire
```

**Noms de fichiers recommandés** :
- `dashboard-main.png` - Tableau de bord principal
- `alerts-page.png` - Page des alertes
- `predictions-page.png` - Page des prédictions
- `kafka-ui.png` - Interface Kafka (optionnel)
- `mongo-express.png` - Interface MongoDB (optionnel)

### Standards de code

- **PEP 8** pour le style Python
- **Commentaires** en français pour la documentation
- **Tests unitaires** pour les nouvelles fonctionnalités
- **Documentation** mise à jour pour les changements API

---

## 📞 Support et contact

- **Documentation** : Ce README et les commentaires dans le code
- **Issues** : Utilisez les GitHub Issues pour rapporter des bugs
- **Discussions** : GitHub Discussions pour les questions générales
- **Email** : [contact@maintenance-predictive.com](mailto:contact@maintenance-predictive.com)

---

**Créé par l'équipe de Maintenance Prédictive** - 2024  
**Licence** : MIT  
**Version** : 1.0.0

> 💡 **Astuce** : Consultez les logs des services Docker avec `docker-compose logs -f` pour diagnostiquer les problèmes de connexion.
