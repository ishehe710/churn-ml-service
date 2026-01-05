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

from fastapi import FastAPI
from load_model import model
from src.ml.features import map_churn_input_to_df
from src.api.schema import ChurnInput

# api stuff
app = FastAPI()

@app.post('/predict')
def predict(data: ChurnInput):
    
    # predict the user input
    sample = map_churn_input_to_df(data)
    pred = model.predict(sample)[0]
    pred_proba = model.predict_proba(sample)[0, 1]
    
    return {'churn': bool(pred), 'probability': float(pred_proba)}