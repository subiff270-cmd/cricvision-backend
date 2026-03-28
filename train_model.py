import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Dummy training data
data = pd.DataFrame({
    "score": [50, 80, 120, 150, 180, 200],
    "wickets": [1, 2, 3, 4, 5, 6],
    "overs_left": [15, 12, 10, 8, 5, 3],
    "win": [0, 0, 1, 1, 1, 1]
})

X = data[["score", "wickets", "overs_left"]]
y = data["win"]

model = LogisticRegression()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully")