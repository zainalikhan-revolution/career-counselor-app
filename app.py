import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load your dataset
data = pd.read_csv('career_data.csv')

# Simple label encoding for interest and skills
data['interest'] = pd.factorize(data['interest'])[0]
data['skills'] = pd.factorize(data['skills'])[0]

# Features and target
X = data[['interest', 'skills']]
y = data['recommended_career']

# Train the model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save the model to a file
with open('model/career_model.pkl', 'rb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as career_model.pkl")
