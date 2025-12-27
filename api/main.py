from fastapi import FastAPI
import joblib
import pandas as pd

# load model
model = joblib.load('../models/churn_model.joblib')

# api stuff
api = FastAPI()

@api.post('/predict')
def predict(data: dict):
    # loaded churn model
    print('Model loaded successfully.')
    
    # predict the user input
    sample = pd.DataFrame([data])
    pred = model.predict(sample)
    pred_proba = model.predict_proba(sample)[0][1]
    
    return {'churn_prediction': str(pred[0]), 'churn_probability': str(pred_proba)}