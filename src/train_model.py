import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from preprocessing import process_data
import joblib


# load data
df = pd.read_csv('../data/processed/telco_churn_clean.csv')

# appylying preprocessing for model
df = process_data(df)

X = df.drop('Churn', axis=1)
y = df['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# training the model
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

# save trained model
joblib.dump(model, '../models/churn_model.joblib')
print("The churn model was saved successfully.")