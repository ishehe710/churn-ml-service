
# Customer Churn Predictor Using Machine Learning

## Problem Statement 

Customer churn refers to customers discontinuing their use of a company’s products or services. It is a critical business metric, as high churn rates directly impact revenue, growth, and long-term sustainability. This issue is especially important in subscription-based industries, where retaining existing customers is often more cost-effective than acquiring new ones.

In this project, I build a machine learning–based customer churn prediction system to help businesses identify customers who are at high risk of churning. The task is formulated as a binary classification problem, where the target variable indicates whether a customer has churned.

The goal of this project is not only to develop accurate predictive models, but also to translate predictions into actionable business insights that can support proactive retention strategies and performance monitoring.

## API & SQL Desgin

This project implements uses an API to connect the machine learning model to the web application.

### API
- I will be using FASTAPI to implement this process.
- The API connects the customer churn predicting model to the web application.
- It has a POST request that sends feature value data to the model.
- The input is a JSON that holds feature values for the model
    * Example:
    `
        {
            "TotalCharges": 29.85,
            "Month-to-Month (Contract)": 1,
            "tenure": 1,
            "SeniorCitizen": 0,
            "Two year (Contract)": 0 
        }
    `
- The output is a JSON that holds the prediction and the churn label.
    * Example:
    `
        {
            churn_probability: 0.82,
            churn_prediction: "High Risk"
        }
    `

### Saving the Model
I will save the best trained model using **Joblib**. Joblib is an open source python library used to optimize computational tasks through parallel computing, disk-caching, and efficient data storage. For this project I will use it to save the best churn predicting model and use it for the application.

### SQL Design
- I will be using SQLite, since it is lightweight and does not require a server.
- There will be two tables for the database. One called customers and another called predictions.
    * **customers**: Each document in the collection of customers will contain the customer ID and all of the feature values used for the model prediction. 
    * **predictions**: Each document in this collection will contain the customer ID, the prediction of whether they churned or not, the churn probability, and the timestamp of the predicition.
- Some query examples:
    * High-Risk Customers
    `
        SELECT customer_id, churn_probability
        FROM predictions
        WHERE churn_prediction = 1
        ORDER BY churn_probability DESC;
    `
    * 
    `
        SELECT DATE(timestamp), COUNT(*)
        FROM predictions
        GROUP BY DATE(timestamp);
    `

### End-to-End System Flow
- The user provides input for a customer with selected feature values.
- This is then sent as a POST request to the API to the `/predict` endpoint.
- The the model that was saved will be load and gives the prediction probailty from the data sent.
- Then then it sends the output prediction and probability.


