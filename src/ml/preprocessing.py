"""
preprocessing.py

Owns:
- Numeric scaling
- Categorical encoding

Does NOT:
- Load models
- Perform predictions
- Know about FastAPI
- Have the mapping function for ChurnInput
"""

import pandas as pd

# processes the cleaned csv file to be used for model input
def process_data(df):
    categorical_cols = df.select_dtypes(include='object').columns 
    for c in categorical_cols:
    
        # encoding
        hot_encoded_c = pd.get_dummies(df[c])
        new_categories = hot_encoded_c.columns
    
        # new categories for df
        new_categories_distinct = [ f"{new_c} ({c})" for new_c in new_categories]
        hot_encoded_c.columns = new_categories_distinct
    
        # creating the new categories
        df[new_categories_distinct] = hot_encoded_c
        df = df.drop(columns=[c])

    return df