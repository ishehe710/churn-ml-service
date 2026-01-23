# Customer Churn Predictor Using Machine Learning

## Problem Statement

Customer churn occurs when customers discontinue their use of a company’s products or services. High churn rates directly impact revenue, growth, and long-term sustainability, making churn a critical business metric. Retaining existing customers is often more cost-effective than acquiring new ones, particularly in subscription-based industries.

This project implements a machine learning–based system to predict customer churn, helping businesses identify high-risk customers. The task is framed as a binary classification problem, where the target variable indicates whether a customer has churned.

The goal is not only to develop accurate predictive models but also to translate predictions into actionable insights to support proactive retention strategies and performance monitoring.

---

## System Architecture

A detailed breakdown of the system design, module responsibilities, and data flow can be found in:

➡️ **[architecture.md](./docs/architecture.md)**

---

## API & SQL Design

### API

- Implemented using **FastAPI**
- Exposes a machine learning model through a REST interface
- **POST** endpoint: `/predict`
- Accepts model-ready features and returns churn risk

**Example Request**
```json
{
  "TotalCharges": 29.85,
  "Month-to-Month (Contract)": 1,
  "tenure": 1,
  "SeniorCitizen": 0,
  "Two year (Contract)": 0,
  ...
}
```

**Example Response**
```json
{
  "churn_label": 1, 
  "probability": 0.452534225,
  "model_version": "LogisticRegression"
}
```

---

### Model Packaging

- Final model is serialized using **Joblib**
- Model is loaded once at API startup (no retraining during inference)
- Ensures consistent preprocessing between training and inference

---

### SQL Design

- **Database:** SQLite (lightweight, serverless, ideal for prototyping)
- **Tables:**
  - `predictions`: Churn probability, prediction label, timestamp, model version

**Example Queries**
```sql
SELECT customer_id, churn_probability
FROM predictions
WHERE churn_prediction = 1
ORDER BY churn_probability DESC;
```

```sql
SELECT DATE(timestamp), COUNT(*)
FROM predictions
GROUP BY DATE(timestamp);
```

---

## End-to-End Flow

1. User submits customer data via API or GUI
2. API loads the persisted model
3. Model generates churn probability and risk label
4. Prediction is returned to the client
5. Customer data and predictions are stored in SQLite

---

## Running the Project

### API

```bash
git clone <repo_url>
cd churn-ml-service
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

### GUI (Streamlit)

The GUI provides a lightweight visual wrapper for testing model inference.

```bash
python -m streamlit run src/gui/app.py
```

---

## Logging

The system includes structured logging across:
- API initialization
- Model loading
- Database initialization
- Prediction events

This ensures traceability and debuggability across the entire pipeline.

---

## Model Results

| Model                                | Accuracy | Recall (Churn) | Precision (Churn) | F1-score (Churn) | Notes |
|-------------------------------------|----------|----------------|-------------------|------------------|-------|
| Logistic Regression (Baseline)      | 0.79     | 0.51           | 0.62              | 0.56             | Baseline |
| Logistic Regression (Class Weights) | 0.74     | 0.79           | 0.50              | 0.62             | **Selected model** |
| Random Forest Classifier            | 0.78     | 0.45           | 0.61              | 0.52             | Lower recall |

### Model Selection Rationale

The **Logistic Regression model with class weighting** was selected despite a small drop in overall accuracy. The primary business objective is identifying at-risk customers, making **recall and F1-score for the churn class** more important than raw accuracy.

This model provides:
- Stronger detection of churned customers
- Better alignment with retention-focused use cases
- Simpler interpretability for stakeholders

---

## Future Improvements

1. Advanced model experiments (cross-validation, hyperparameter tuning)
2. Neural networks using PyTorch
3. Migration from SQLite to PostgreSQL for production scaling
4. Expansion into CLV and multi-task prediction
5. More robust frontend (React or enhanced Streamlit)

---

## Project Status

✅ Complete and production-structured  
🧹 Polished for portfolio presentation  
🚀 Ready for extension into larger ML systems
