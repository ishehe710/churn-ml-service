# App Architecture & Boundaries

All production code for the churn-ml-service lives under the `src/` directory. This document defines architectural boundaries and ownership rules for each component.

## App Architecture Explained
- The API for this project takes customer input of 46 feature values and outputs a JSON with the predicted churn label and churn probability.
- The folders of the app:
    - `src/api/`: handles the routing of data, input and output of the model, etc and it acts as the controller of the application.
    - `src/ml/`: this folder contains the necessary machine learning objects, such as the saving and loading the churn model, preprocessing data functionality, and a schema to represent the contract between the customer input and model features.
    - `src/models/`: holds the actual saved models for the churn service.
- The model training happens offline, outside the API.

## Purpose of Each File in Project
Every file in the src folder should have their own unique purpose and I describe the boundaries of each file for that to be true.
- `main.py`: Holds the routing for the api and only that. Does not contain or depend on training logic or preprocessing logic. This is in the `src/api/` folder.
- `schema.py`: Holds the contract for customer input shape and types, but not business logic or feature ordering. This is in the `src/api/` folder.
- `features.py`: contains all the features of model in exact order and has the mapping function for ChurnInput to model features. The feature order defined here must exactly match the model’s expected input order. This is in the `src/ml/` folder.
- `preprocessing.py`: holds the function that processes the cleaned csv file to then be used for the churn model for trainning. Used only during training, never at inference time. This is in the `src/ml/` folder.
- `train_model.py`: trains the churn model for the project and saves it to then be loaded later. This is in the `src/ml/` folder.
- `load_model.py`: loads the churn model saved from train_model.py to then be used in the api. This file is the single source of truth for how models are loaded in the application. This is in the `src/ml/` folder.
- `logging_config.py`: holds the configuration of a local logger for the necessary files of the project. Files `main.py` and `load_model.py` use it the logger to ensure the API is running correctly. This file is found in the `src/api` folder.
- `validators.py`: holds the validation of user customer churn input to have fields that are mutually exclusive to be selected at the same time, else it throws an error. This file is found in the `src/api` folder.

## Expectations of the Application
- The request field for the POST `/predict` endpoint takes a JSON of 46 feature values denoted by the ChurnInput schema in schema.py.
- The output of the `/predict` endpoint is a JSON of the prediction label and the probability.
- **1** means customer churn and **0** means customer is still purchasing a service from the company.
- Determining customer label if the model outputs a probability as p:
    - If `p >= 0.75`, &rarr; extreme risk of churning.
    - Else if `0.5 <= p < 0.75`, &rarr; high risk of churning.
    - Else if `0.25 <= p < 0.5`, &rarr; low risk of churning.
    - Else not at risk of churning.

## Details on Logging

### What is Logged?
Details on what should be logged and what to log.

- During inference
    - Model succefully predicts
    - Model fails to predict
    - Invalid inputs
- Information safe to log
    - Whether the inference was succesful
    - Time of log
    - Derived output only (prediction label, probability), never raw features
- Information not safe to log
    - customer input information
    - details about the model

### Where Should Logging Happen?
Deciding the boundaries of where logging to should happen in the app.

- API Layer: To log when request was recieved and when the output happens.
- Model Loader: To log when the model is loaded and which model artifact/version is active.
- Error: If there was a invalid request where the values for model features do not meet model requirements.

No logging inside training phase of the model and the mapping of ChurnInput to model features.

### Log Format
I will use a JSON to format the logging information.
- For example:
    - 
    ```json
    {
        "event": "request_received",
        "level": "info",
        "timestamp": "2026-01-07T20:38:25.203425"
    }
    ```

### Encapsulation of the Logging Configuration
There will be a sperate file for logging information, with the log design and funcitonality. Then it will be invoked by an import into files `main.py` and other necessary files.

## Phase 4 Reflection

### Things I learned About Implementing API for This Churn Project
I was able to make designs in API that overcame potential issues in future. For example, I modularized tasks for the API: having seperate files for loggging configuration, routing, loading model, training model, and other necessary functionality. 

By doing this, I was able to more easily modify code and identify issues when the API crashed.

### Tradeoffs in API Design Decisions

One deliberate design decision was to use structured JSON logging rather than plain string-based logs.

The primary benefit of JSON logs is that they are machine-parseable and can be easily ingested by log aggregation or analysis systems in production. This enables filtering, aggregation, and correlation across requests, which would be significantly harder with unstructured logs.

A tradeoff of this approach is reduced human readability when viewing logs directly during local development. While JSON logs are less visually pleasing in a terminal, this cost was accepted in favor of improved observability and future scalability.

Given that this project prioritizes production-oriented design, structured logging was chosen intentionally despite its verbosity.
