import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

# Load dataset
data = pd.read_csv('career_data.csv')

# Encode categorical variables
le_interests = LabelEncoder()
le_skills = LabelEncoder()
le_environment = LabelEncoder()
le_career = LabelEncoder()

data['interests_enc'] = le_interests.fit_transform(data['interests'])
data['skills_enc'] = le_skills.fit_transform(data['skills'])
data['environment_enc'] = le_environment.fit_transform(data['preferred_environment'])
data['career_enc'] = le_career.fit_transform(data['career_path'])

# Features and target
X = data[['interests_enc', 'skills_enc', 'marks', 'environment_enc']]
y = data['career_enc']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)
import pickle

with open('career_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model saved!")

# Save model and encoders
os.makedirs('model', exist_ok=True)
with open('model/career_model.pkl', 'wb') as f:
    pickle.dump({
        'model': model,
        'le_interests': le_interests,
        'le_skills': le_skills,
        'le_environment': le_environment,
        'le_career': le_career
    }, f)
