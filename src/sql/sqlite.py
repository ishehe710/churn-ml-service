"""
sqlite.py

Owns:
- Initialization of the churn SQL database

Does Not: 
- Logging configurations
- Routing
- ChurnInput schema
- Load or train models
"""

from src.api.persistence import PredictionStore
from src.api.logging_config import get_logger

# initializing logger
db_logger = get_logger(__name__)

# intialilizing churn database 
db = PredictionStore()
db_logger.info("database_connected")    

