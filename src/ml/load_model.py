"""
main.py

Owns:
- Routing for the application
- Performs the predictions
- Peforms the mapping of ChurnInput into model features

Does NOT:
- Have functionality of preprocessing data
- Train the model & save it
- Load the model
"""

import joblib

# load model
model = joblib.load('./src/models/churn_model.joblib')
print('Model loaded successfully.')
