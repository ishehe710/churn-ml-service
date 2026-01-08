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
from src.api.logging_config import get_logger

MODEL_PATH = "./src/models/churn_model_v1.joblib"

model_loader_logger = get_logger(__name__)

# load model
model_loader_logger.info("starting_load")
model = None

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model_loader_logger.error("load_failed", error=str(e))
    raise

model_loader_logger.info(
    "model_loaded",
    model_path=MODEL_PATH,
    model_type=type(model).__name__,
    model_name=getattr(model, "custom_name", "unknown")
)
