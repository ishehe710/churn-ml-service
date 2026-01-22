# App Architecture & Boundaries

All production code for the churn-ml-service lives under the `src/` directory. This document defines architectural boundaries, ownership rules, and design decisions for each component of the system.

---

## 1. High-Level System Overview

The churn-ml-service is a production-oriented machine learning inference system with the following responsibilities:

- Accept structured customer feature inputs
- Produce churn probability and churn risk classification
- Persist derived prediction metadata for traceability
- Expose a clean API and GUI interface

**Key principle:**  
The API acts strictly as an *orchestrator*. It does not own business logic, model logic, or feature engineering decisions.

---

## 2. Application Architecture

### Directory Structure
```
src/
├── api/        # Request handling, validation, orchestration, logging
├── ml/         # Model loading, feature contracts, training utilities
├── models/     # Serialized model artifacts
├── sql/        # Database initialization and storage adapters
├── gui/        # Streamlit-based user interface
```

### Architectural Flow
```
GUI → API → Feature Mapping → Model Inference → Persistence → Response
```

---

## 3. Component Ownership & Boundaries

### `src/api/` — API Layer (Controller)
**Owns:**
- HTTP routing (`/predict`)
- Input validation
- Logging
- Orchestration of inference flow
- Calling persistence layer

**Does NOT:**
- Train models
- Define feature order
- Perform preprocessing
- Contain ML logic

**Files:**
- `main.py`: API routing only
- `schema.py`: Request/response contracts
- `validators.py`: Input consistency checks
- `logging_config.py`: Centralized logging setup
- `persistence.py`: Database interface abstraction

---

### `src/ml/` — Machine Learning Layer
**Owns:**
- Feature contracts and ordering
- Model loading
- Offline training utilities

**Does NOT:**
- Handle HTTP
- Perform persistence
- Know about FastAPI or Streamlit

**Files:**
- `features.py`: Immutable feature contract and ordering
- `load_model.py`: Single source of truth for model loading
- `train_model.py`: Offline model training
- `preprocessing.py`: Training-only data preprocessing

**Feature Contract Rule:**  
The feature order defined in `features.py` is immutable once a model is trained. Any change requires retraining and version bumping.

---

### `src/sql/` — Persistence Layer
**Owns:**
- Database initialization
- Storage of prediction metadata

**Files:**
- `sqlite.py`: SQLite database initialization and lifecycle management

---

### `src/gui/` — User Interface
**Owns:**
- User interaction
- API communication
- Presentation logic

**Files:**
- `app.py`: Streamlit GUI
- `api_client.py`: HTTP client for API communication

---

## 4. API Contract

### `/predict` Endpoint
**Input:**
- JSON payload of 46 features defined by `ChurnInput`

**Output:**
```json
{
  "probability": 0.82,
  "churn_label": 1,
  "model_version": "LogisticRegression"
}
```

### Risk Interpretation
- `p ≥ 0.75` → Extreme churn risk
- `0.5 ≤ p < 0.75` → High churn risk
- `0.25 ≤ p < 0.5` → Low churn risk
- `p < 0.25` → Not at risk

---

## 5. Logging Design

### What Is Logged
- Request received
- Successful inference
- Failed inference
- Validation errors
- Model load events

### Safe to Log
- Timestamps
- Request identifiers
- Derived outputs only (label, probability)
- Model version

### Never Logged
- Raw customer features
- Personally identifiable information
- Model internals or parameters

### Log Format
Structured JSON logs (example for successful prediction):
```json
{
    "latency_ms": 4.6665, 
    "num_samples": 1, 
    "event": "prediction_completed", 
    "level": "info", 
    "timestamp": "2026-01-21T20:26:51.462776"}
```

---

## 6. SQL Design & Persistence Strategy

### Purpose of Persistence
- Traceability of predictions
- Reproducibility across model versions
- Auditing of inference outcomes

### Why SQLite
- Minimal setup overhead
- Suitable for single-user and local inference workloads
- Easily replaceable with Postgres in future deployments

### Stored Entities
- Prediction probability
- Churn label
- Model version
- Request identifier
- Timestamp

### Explicit Exclusions
- Raw input features
- User identity
- Analytical aggregates

### Schema Concept
```sql
predictions
-----------
id (PK)
request_id (UUID)
model_version (TEXT)
prediction (REAL)
churn_label (INTEGER)
created_at (TIMESTAMP)
```

### Priority of Prediction Over Persistence
Persistence failures never block prediction delivery. Database writes are wrapped in non-fatal error handling with proper logging.

---

## 7. Reproducibility Guarantees

A prediction is reproducible if:
- The same model artifact is used
- The feature contract is unchanged
- The same feature values are supplied

The system does not guarantee reproducibility across:
- Feature contract changes
- Model retraining without versioning

---

## 8. Phase Reflection

### Key Learnings
- Clear separation of concerns simplifies debugging and iteration
- Treating ML inference as a production system improves design discipline
- Explicit architectural boundaries prevent feature creep

### Tradeoffs
- JSON logging trades readability for machine-parsability
- SQLite trades scalability for simplicity
- Strict feature contracts require disciplined versioning

These tradeoffs were chosen intentionally to align with production best practices while keeping the project manageable.

---

## 9. Future Extensions
- Replace SQLite with Postgres
- Add batch inference
- Introduce CLV modeling
- Implement model monitoring and drift detection
