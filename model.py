import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle


data = pd.read_csv("data.csv")

X = data.drop("failure", axis=1)
y = data["failure"]

model = RandomForestClassifier()
model.fit(X, y)


pickle.dump(model, open("model.pkl", "wb"))

print("Model trained successfully!")