# App Architecture & Boundaries

All production code for the churn-ml-service lives under the src/ directory. This document defines architectural boundaries and ownership rules for each component

## App Architecture Explained
- The API for this project takes customer input of 46 feature values and outputs a JSON with the predicted churn label and churn probability.
- The folders of the app:
    - api: handles the routing of data, input and output of the model, etc and it acts as the controller of the application.
    - ml: this folder contains the necessary machine learning objects, such as the saving and loading the churn model, preprocessing data functionality, and a schema to represent the contract between the customer input and model features.
    - models: holds the actual saved models for the churn service.
- The model training happens outside the API and is offline.

## Purpose of Each File in Project
Every file in the src folder should have their own unqie purpose and I described the boundaries of each file for that to be true.
- **main.py**: holds the routing for the api and only that. Does not contain or depend on training logic or preprocessing logic. This is in the api folder.
- **schema.py**: holds the contract between customer input and the model interface. This is in the api folder.
- **features.py**: contains all the features of model exactly and has the mapping function for ChurnInput to model features. The feature order defined here must exactly match the model’s expected input order. This is in the ml folder.
- **preprocessing.py**: holds the function that processes the cleaned csv file to then be used for the churn model for trainning. Used only during training, never at inference time. This is in the ml folder.
- **train_model.py**: trains the churn model for the project and saves it to then be loaded later. This is in the ml folder.
- **load_model.py**: loads the churn model saved from train_model.py to then be used in the api. This file is the single source of truth for how models are loaded in the application. This is in the ml folder.

## Expectations of the Application
- The request field for the POST /predict endpoint takes a JSON of 46 feature values denoted by the ChurnInput schema in schema.py.
- The output of the /predict endpoint is a JSON of the prediction label and the probability.
- 1 means customer churn and 0 means customer is still purchasing a service from the company.
- Determining customer label if the model outputs a probability as p:
    - If `p >= 0.75`, &rarr; extreme risk of churning.
    - Else if `0.5 <= p < 0.75`, &rarr; high risk of churning.
    - Else if `0.25 <= p < 0.5`, &rarr; low risk of churning.
    - Else not at risk of churning.

## Potential Issues of the App
- Invalid inputs: incorrect values or logically incoherent values.
    - Like a customer being two year contract and a month-to-month one at the same time.
- Schema drift (training features vs API schema)
- Model version mismatch (wrong model loaded)

## Refactoring Task for Tomorrow
Introduce structured logging across API and model inference paths.

