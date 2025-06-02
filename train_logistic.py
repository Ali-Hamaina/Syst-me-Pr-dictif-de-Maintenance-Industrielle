import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

print("🔧 Training logistic regression model...")

# Données d'exemple (4 features + target)
data = pd.DataFrame({
    "volt": [10.5, 11.0, 12.3, 9.8],
    "rotate": [1000, 1050, 980, 990],
    "pressure": [30.5, 32.0, 31.0, 29.8],
    "vibration": [0.02, 0.03, 0.025, 0.015],
    "status": [0, 1, 0, 1]  # 0 = OK, 1 = failure
})

X = data[["volt", "rotate", "pressure", "vibration"]]
y = data["status"]

# Entraînement d'un modèle de régression logistique
model = LogisticRegression(random_state=42)
model.fit(X, y)

# Sauvegarde du modèle
with open("model_logistic.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Modèle logistique entraîné et sauvegardé dans model_logistic.pkl")