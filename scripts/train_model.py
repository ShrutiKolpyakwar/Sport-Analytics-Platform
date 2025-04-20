import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 📌 Your existing player performance data
data = {
    "Name": ["Cristiano Ronaldo", "Lionel Messi", "Kylian Mbappe", "Neymar Jr", "Bruno Fernandes"],
    "Matches Played": [32, 30, 29, 25, 31],
    "Goals": [28, 25, 22, 19, 15]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Feature (Matches Played) and Target (Goals)
X = df[["Matches Played"]]
y = df["Goals"]

# Train Model
model = LinearRegression()
model.fit(X, y)

# Save Model
joblib.dump(model, "stats/ml_models/goals_predictor.pkl")

print("Model trained and saved successfully!")
