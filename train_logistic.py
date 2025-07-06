import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

print("🔧 Training logistic regression model for refrigeration systems...")

# Données d'exemple pour installations frigorifiques (paramètres thermodynamiques)
data = pd.DataFrame({
    "temp_evaporator": [-10.5, -8.0, -12.3, -15.8, -7.2, -11.0, -9.5, -13.1, -6.8, -14.2],  # Température évaporateur (°C)
    "temp_condenser": [40.5, 38.0, 45.3, 42.8, 39.2, 44.0, 41.5, 46.1, 37.8, 47.2],        # Température condenseur (°C)
    "pressure_high": [12.5, 11.8, 14.2, 13.1, 12.0, 13.8, 12.7, 14.5, 11.5, 15.0],         # Pression haute (bar)
    "pressure_low": [2.1, 2.3, 1.8, 1.9, 2.4, 1.7, 2.2, 1.6, 2.5, 1.5],                    # Pression basse (bar)
    "superheat": [8.5, 9.2, 7.8, 6.9, 9.8, 7.2, 8.9, 6.5, 10.1, 6.2],                      # Surchauffe (°C)
    "subcooling": [5.2, 4.8, 6.1, 5.7, 4.5, 6.3, 5.0, 6.8, 4.2, 7.1],                      # Sous-refroidissement (°C)
    "compressor_current": [8.2, 7.9, 9.5, 8.8, 7.6, 9.2, 8.5, 9.8, 7.4, 10.1],            # Courant compresseur (A)
    "vibration": [0.02, 0.03, 0.025, 0.015, 0.035, 0.018, 0.028, 0.042, 0.038, 0.045],     # Vibrations (g)
    "status": [0, 0, 1, 1, 0, 1, 0, 1, 0, 1]  # 0 = OK, 1 = défaillance
})

X = data[["temp_evaporator", "temp_condenser", "pressure_high", "pressure_low", 
          "superheat", "subcooling", "compressor_current", "vibration"]]
y = data["status"]

# Entraînement d'un modèle de régression logistique pour installations frigorifiques
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X, y)

# Sauvegarde du modèle
with open("model_logistic_refrigeration.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Modèle logistique pour installations frigorifiques entraîné et sauvegardé dans model_logistic_refrigeration.pkl")
print(f"📊 Précision du modèle: {model.score(X, y):.2%}")
print("🧊 Paramètres surveillés: Température évaporateur/condenseur, pressions, surchauffe, sous-refroidissement, courant compresseur, vibrations")