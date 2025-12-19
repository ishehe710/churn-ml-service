import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("../data/raw/telco_churn.csv")  # adjust filename if you kept original

# Connect to SQLite DB (creates file if not exist)
conn = sqlite3.connect("../sql/telco_churn.db")

# Save CSV to SQL table
df.to_sql("customers", conn, if_exists="replace", index=False)

# Test query: count total customers
result = pd.read_sql("SELECT COUNT(*) AS total_customers FROM customers", conn)
print(result)

# Count churned customers
pd.read_sql("SELECT Churn, COUNT(*) FROM customers GROUP BY Churn", conn)

# Average tenure
pd.read_sql("SELECT AVG(tenure) AS avg_tenure FROM customers", conn)

conn.close()

