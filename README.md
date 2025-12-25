# Customer Churn Predictor Using Machine Learning

## Problem Statement 

Customer churn refers to customers discontinuing their use of a company’s products or services. It is a critical business metric, as high churn rates directly impact revenue, growth, and long-term sustainability. This issue is especially important in subscription-based industries, where retaining existing customers is often more cost-effective than acquiring new ones.

In this project, I build a machine learning–based customer churn prediction system to help businesses identify customers who are at high risk of churning. The task is formulated as a binary classification problem, where the target variable indicates whether a customer has churned.

The goal of this project is not only to develop accurate predictive models, but also to translate predictions into actionable business insights that can support proactive retention strategies and performance monitoring.

---

## API & SQL Design

### API

- I will be using **FastAPI** to implement this process.
- The API connects the customer churn predicting model to the web application.
- It has a **POST** request that sends feature value data to the model.
- The input is a JSON that holds feature values for the model.  
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
- The output is a JSON that holds the prediction and the churn label.  
  Example:
```json
{
    "churn_probability": 0.82,
    "churn_prediction": "High Risk"
}
```

### Model Packaging

- The best trained model will be saved using **Joblib**, which allows fast loading for inference without retraining.
- Ensures that preprocessing steps are consistent between training and inference.
- Deliverable: The model is saved once and loaded for predictions.

### SQL Design

- **Database Choice:** SQLite (lightweight, no server needed)
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

```mermaid
flowchart TD
    A[User / Frontend] -->|Input customer features| B[POST /predict API Endpoint]
    B --> C[Load Saved Model (Joblib)]
    C --> D[Make Prediction & Compute Probability]
    D --> E[Return JSON Response to Frontend]
    D --> F[Store in SQLite Database: Customers & Predictions Tables]
```

**Explanation:**

- **A → B:** User inputs customer data via the frontend and sends it as a POST request.  
- **B → C:** The API loads the saved model (no retraining).  
- **C → D:** Model predicts churn probability and label.  
- **D → E:** Prediction JSON is returned to the frontend.  
- **D → F:** Prediction data is saved to the database.  
- **F → G/H:** Data is organized into `predictions` and `customers` tables.

---

## Notes

- This README is a living document and will be updated as the project progresses.
- All ML models, API endpoints, and SQL designs are aligned to ensure consistent reproducibility and ease of deployment.
- This document serves as both technical documentation and portfolio reference for internships or job applications.
