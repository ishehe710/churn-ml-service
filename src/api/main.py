# other imports
from fastapi import FastAPI
import joblib
from src.ml.features import map_churn_input_to_df
from src.api.schema import ChurnInput

# load model
model = joblib.load('./src/models/churn_model.joblib')
print('Model loaded successfully.')

# api stuff
app = FastAPI()

@app.post('/predict')
def predict(data: ChurnInput):
    
    # predict the user input
    sample = map_churn_input_to_df(data)
    pred = model.predict(sample)
    pred_proba = model.predict_proba(sample)[0][1]
    
    return {'churn': str(pred[0]), 'probability': str(pred_proba)}