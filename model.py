import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("diabetes.csv")

X = data.drop(columns="Outcome", axis=1)
Y = data["Outcome"]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, Y_train, Y_test = train_test_split(
    X_scaled, Y, test_size=0.2, stratify=Y, random_state=2
)

# Model
model = SVC(kernel="linear", probability=True)
model.fit(X_train, Y_train)

print("Training Accuracy:", accuracy_score(Y_train, model.predict(X_train)))
print("Testing Accuracy:", accuracy_score(Y_test, model.predict(X_test)))

# Save
pickle.dump(model, open("diabetes_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("Model & Scaler saved successfully")
