"""
persistance.py

Owns:
- Persistance of requests and their outputs

Does Not: 
- Logging configurations
- Routing
- ChurnInput schema
"""

import sqlite3
import uuid
from pathlib import Path
from typing import Optional

from src.api.logging_config import get_logger

logger = get_logger(__name__)

# Resolve project root safely (…/src/api/persistance.py → project root/src)
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "sql" / "churn.db"


class PredictionStore:
    """
    Best-effort persistence layer for churn predictions.

    Responsibilities:
    - Persist derived outputs only (no raw inputs)
    - Never block inference if persistence fails
    - Provide traceability via request_id and model_version
    """

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        """
        Create the predictions table if it does not exist.
        Safe to call multiple times.
        """
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY,
                        request_id TEXT NOT NULL,
                        model_version TEXT NOT NULL,
                        prediction REAL NOT NULL,
                        churn_label INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                conn.commit()

            logger.info("db_initialized", db_path=str(self.db_path))

        except Exception as e:
            logger.error("db_initialization_failed", error=str(e))

    def save_prediction(
        self,
        model_version: str,
        prediction: float,
        churn_label: int,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Persist a churn prediction.

        This method must never raise.
        """
        request_id = request_id or str(uuid.uuid4())

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO predictions (
                        request_id,
                        model_version,
                        prediction,
                        churn_label
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        request_id,
                        model_version,
                        prediction,
                        churn_label,
                    ),
                )
                conn.commit()

            logger.info(
                "prediction_persisted",
                request_id=request_id,
                model_version=model_version,
            )

        except Exception as e:
            # Best-effort persistence: log and continue
            logger.error(
                "prediction_persistence_failed",
                request_id=request_id,
                error=str(e),
            )
