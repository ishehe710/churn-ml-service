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
- `logging_config.py`: holds the configuration of a local logger for the necessary files of the project. Files `main.py` and `load_model.py` use it the logger to ensure the API is running correctly. This file is found in the `src/api/` folder.
- `validators.py`: holds the validation of user customer churn input to have fields that are mutually exclusive to be selected at the same time, else it throws an error. This file is found in the `src/api` folder.
- `persistence.py`: holds the SQL database intialization as a class called **PredictionStore** and exports it to `sqlite.py`. This file is held in `src/api/`.
- `sqlite.py`: holds the initialization of the SQL database for the churn project which is then exported to the api for usage. This file is in the `src/sql/`.
- `app.py`: holds the GUI code for the churn risk predictor project. This file is in the folder `src/gui/`.
- `api_client.py`: holds the link between the GUI wrapper of the application and the API to call the model.  This file is in the folder `src/gui/`.

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

## SQL Design and Implementation
I this section I will go over how I designed the SQL database for the churn project, the decisions made and what tradeoffs I considerd.

### Purpose of SQL Datase
The SQL database is incorporated into the project for persistance reasons. This allows the application to have access to recorded input and output from the churn model inside the API. This persistance for record keeping allows gives the project traceability and reproducibility. First, by recording a request identifier and derived outputs and output we have direct record of information for one request. Then for reproducibility, we can reproduce predictions under the same model version and feature contract to get the same output to show reproducable the results are.

### Why SQLite Over Postgres
For this churn project I decided to use SQLite for database. I choose this over Postgres for a couple of reasons. First was due to the scale of project. The project is a single user and not super complex, thus having to deal with the setup that comes with Postgres and the other features with it are not worth with for the current stage of the project. However the setup of SQLite is pretty quick and easier maintain. But, in the future renditions of the project it is best to make the switch to Postgres.

### What to Persist and Not
I will list the things that are persisted and are not persited

Entities
- Predictions from model
- Model medata
- Key for particular churn input
- Timestamp

Exclusions
- Raw request payloads (for privacy)
- User identity (for privacy)
- Long term analytic data (not focus of project)

### Schema for Persistance
Here I discussed the conceptual SQL Schema for the project.

There are one tables for the database: `predictions`.
- SQL schema concept:
    ```sql
        predictions
        -----------
        id (PK)
        request_id (UUID)
        model_version (TEXT)
        prediction (REAL)
        churn_label (INTEGER or BOOLEAN)
        created_at (TIMESTAMP)
    ```


### Priority of Prediction Over Persistence
There will be a python file called persistence.py in the api folder of the project. Then the database is created in a seperate folder called `src/sql`. This seperates the API and storage of data since there are seperate files for each task. Persistance does not block the end-to-end flow of the application when there are try-except blocks for inserting documents into the database and proper logging for database. Lastly, regardless of the state of the database the service still provides a predicition output.

<!--
Polishing Day TODOs:
- Clarify API role as orchestrator (not business logic owner)
- Explicitly state feature contract immutability
- Refine reproducibility guarantees and assumptions
- Tighten logging safety definitions
- Clarify scope of stored model metadata
-->
