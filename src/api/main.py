"""
main.py

Owns:
- Routing for the application
- Performs predictions
- Invokes mapping of ChurnInput into model features

Does NOT:
- Contain preprocessing logic
- Train or save models
- Contain model loading logic (delegated to load_model.py)
"""


# imports
from fastapi import FastAPI
from src.ml.load_model import model
from src.ml.features import map_churn_input_to_df
from src.api.schema import ChurnInput
from src.api.logging_config import get_logger
import time

# initialize api logger
api_logger = get_logger(__name__)

# api stuff
app = FastAPI()

@app.post('/predict')
def predict(data: ChurnInput):
    
    # logging that request was received
    api_logger.info("request_received")
    
    
    try:
        # mapping customer input to model features
        sample = map_churn_input_to_df(data)
    except Exception as e:
        api_logger.warning("invalid_customer_input", error=str(e))
        raise
    
    api_logger.info(
        "input_mapped_to_features",
        num_features=sample.shape[1],
        feature_names=list(sample.columns)
    )
    
    # capture start time
    start_ns = time.perf_counter_ns()
    
    try:
        # predict the user input
        pred = model.predict(sample)[0]
        pred_proba = model.predict_proba(sample)[0, 1]
    except Exception as e:
        api_logger.error("prediction_failed", error=str(e))
        raise
    
    # calculate latency in milliseconds
    duration_ns = time.perf_counter_ns() - start_ns
    latency_ms = duration_ns / 1_000_000

    
    # logging success of model prediction
    api_logger.info("prediction_completed", latency_ms=round(latency_ms, 4), 
            num_samples=len(sample))
    
    return {'churn': bool(pred), 'probability': float(pred_proba)}