# Customer Churn Predictor Using Machine Learning

## Problem Statement

Customer churn occurs when customers discontinue their use of a company’s products or services. High churn rates directly impact revenue, growth, and long-term sustainability, making churn a critical business metric. Retaining existing customers is often more cost-effective than acquiring new ones, particularly in subscription-based industries.

This project implements a machine learning–based system to predict customer churn, helping businesses identify high-risk customers. The task is framed as a binary classification problem, where the target variable indicates whether a customer has churned.

The goal is not only to develop accurate predictive models but also to translate predictions into actionable insights to support proactive retention strategies and performance monitoring.

---

## API & SQL Design

### API

- Implemented using **FastAPI**.
- Connects the customer churn prediction model to a web application.
- **POST** request endpoint: `/predict`  
- **Input:** JSON containing model-ready feature values.  
  Example:
```json
{
    "TotalCharges": 29.85,
    "Month-to-Month (Contract)": 1,
    "tenure": 1,
    "SeniorCitizen": 0,
    "Two year (Contract)": 0
}
```
- **Output:** JSON containing predicted churn probability and label.  
  Example:
```json
{
    "churn_probability": 0.82,
    "churn_prediction": "High Risk"
}
```

### Model Packaging

- The best trained model is saved using **Joblib** for fast loading during inference.
- Ensures preprocessing consistency between training and inference.
- Model is saved once and loaded for predictions.

### SQL Design

- **Database Choice:** SQLite (lightweight, serverless)
- **Tables:**
  - `customers`: Stores customer ID and all feature values.
  - `predictions`: Stores customer ID, churn prediction, probability, and timestamp.
- **Example SQL Queries:**
  - High-Risk Customers:
```sql
SELECT customer_id, churn_probability
FROM predictions
WHERE churn_prediction = 1
ORDER BY churn_probability DESC;
```
  - Daily Prediction Count:
```sql
SELECT DATE(timestamp), COUNT(*)
FROM predictions
GROUP BY DATE(timestamp);
```

### End-to-End System Flow

- **Frontend → API:** User submits customer data via POST request.  
- **API → Model:** API loads the saved model (no retraining).  
- **Model → Predict:** Model predicts churn probability and label.  
- **Predict → Response:** JSON response is returned to frontend.  
- **Predict → DB:** Prediction data is saved in the database.  
- **DB → Predictions / Customers:** Data is organized into `predictions` and `customers` tables.

### API Usage

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd churn-ml-service
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   cd api
   fastapi dev main.py
   ```
4. Example Request:
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
5. Example Response:
```json
{
    "churn_probability": 0.82,
    "churn_prediction": "High Risk"
}
```

---

## Notes

- This README is a living document and will be updated as the project progresses.
- All ML models, API endpoints, and SQL designs are aligned to ensure reproducibility and ease of deployment.

