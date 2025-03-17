import sys
import pandas as pd
from flask import Flask, request, jsonify
import joblib
import os
from utils import db_setup
import datetime
import csv
import sys
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
from sklearn.preprocessing import LabelEncoder, StandardScaler
warnings.filterwarnings("ignore")
from sklearn.preprocessing import OneHotEncoder
import logging
# Initialize OneHotEncoder
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)  # Use sparse_output instead of sparse
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

def model_initialize():
    global model
    # Load the trained model
    MODEL_PATH = './models/time_based_churn_prediction_model.pkl'
    model = joblib.load(MODEL_PATH)
    return model

csv_file_path = "./data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
log_File_path = "./logs/churn_prediction.log"

def setup_logger(name, log_file):

    """
    Sets up a logger.
    """
    global model
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
log = setup_logger('churn_prediction_api', log_File_path)

@app.route('/predict', methods=['POST'])
def predict():
    """
    API to make churn predictions.
    """
    global model
    client_ip = request.remote_addr  # Capture client's IP address
    log.info(f"Received a prediction request from IP: {client_ip}")
    processed_df=pd.read_csv('dataframe.csv')

    try:
        # Get JSON data from request
        data = request.json
        if not data:
            log.error(f"Missing input data | IP: {client_ip}")
            return jsonify({"error": "No input data provided"}), 400

        log.info(f"Input data received from {client_ip}: {data}")

        # Convert input JSON to DataFrame
        input_data = pd.DataFrame([data])
        print(input_data)
        
        # Ensure input has correct features
        required_features = [ 'Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']

        missing_features = [feature for feature in required_features if feature not in input_data.columns]

        if missing_features:
            log.error(f"Missing required features {missing_features} | IP: {client_ip}")
            return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400      

        # Load processed data (this should be your training dataset)
        processed_df = pd.read_csv("dataframe.csv")  # Ensure this is the training dataset

        # Define categorical features
        categorical_features = [
            'Gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
            'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
            'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 
            'PaperlessBilling', 'PaymentMethod'
        ]

        # **Step 1: Encode Categorical Features for Training Data**
        label_encoders = {}
        for col in categorical_features:
            processed_df[col] = processed_df[col].astype(str)  # Ensure all categorical values are strings
            le = LabelEncoder()
            processed_df[col] = le.fit_transform(processed_df[col])  # Fit & Transform on full dataset
            label_encoders[col] = le  # Store encoder for later use

        # **Step 2: Fit StandardScaler on Processed Data**
        scaler = StandardScaler()
        processed_X = processed_df.drop(columns=['CustomerID'], errors='ignore')
        pd.set_option('display.max_columns', None)  # Show all columns
        processed_X = processed_X.drop(columns=['Churn'], errors='ignore')
        
        # print(processed_X.head())
        scaler.fit(processed_X)  # Fit only once on the full dataset

        # **Step 3: Define Prediction Function**
        def predict_churn(input_data):
            global model
            try:
                input_df = input_data.copy()

                for col in categorical_features:
                    if col in input_df.columns and col in label_encoders:
                        input_df[col] = input_df[col].astype(str).map(lambda x: label_encoders[col].classes_.tolist().index(x) if x in label_encoders[col].classes_ else -1)

                input_df['TotalCharges'] = pd.to_numeric(input_df['TotalCharges'], errors='coerce')
                input_df.fillna(processed_X.median(numeric_only=True), inplace=True)
                input_X = input_df.drop(columns=['CustomerID'], errors='ignore')
                input_X = scaler.transform(input_X)
                try:
                    # Load the trained model
                    with open('./models/time_based_churn_prediction_model.pkl', 'rb') as f:
                        model_rf: RandomForestClassifier = pickle.load(f)

                    # model = joblib.load("./models/time_based_churn_prediction_model.pkl")  # Adjust filename as needed
                except Exception as e:
                    print(f"Error loading model: {e}")
                    model = None  # Ensure the function doesn't run if the model is missing

                # print("~~~~~~~~~~~~~~~~~~~~~~",type(model))
                prediction = model['model'].predict(input_X)
                result_df = input_df[['CustomerID']].copy()
                # result_df[['Churn_30', 'Churn_60', 'Churn_90']] = predictions
                result_df['Churn'] = prediction
                result_df.to_csv('predicted_churn.csv', index=False)
                return result_df
            except Exception as e:
                # print("!!!!!!!!!!!!", e) 
                log.error(f"Error during prediction | IP: {client_ip} | Error: {str(e)}", exc_info=True)         
            # return result_df
        prediction=predict_churn(input_data)
        print(prediction)
        json_data = prediction.to_json(orient="records")
        # Predict churn probability
        # prediction = model.predict(input_X)
        log.info(f"Prediction made for {client_ip}: {json_data}")

        log.info(f"Input data validated successfully from {client_ip}")
        return jsonify({"response": json_data}), 200

    except Exception as e:
        log.error(f"Error during prediction | IP: {client_ip} | Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# API to fetch log files
@app.route('/get_logs', methods=['GET'])
def get_logs():
    global model
    """
    API to fetch log files with client IP tracking.
    """
    client_ip = request.remote_addr  # Get client's IP address
    log.info(f"API Accessed: /get_logs from IP: {client_ip}")

    try:
        # Check if the log file exists
        if not os.path.exists(log_File_path):
            log.warning(f"Log file not found. Accessed by IP: {client_ip}")
            return jsonify({"error": "Log file not found"}), 404

        # Read the log file
        with open(log_File_path, 'r') as log_file:
            log_contents = log_file.read()

        log.info(f"Log file successfully retrieved by {client_ip}")

        # Return the log contents as a plain text response
        return log_contents, 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        log.error(f"Error reading log file: {e} | IP: {client_ip}")
        return jsonify({"error": str(e)}), 500

def write_to_csv(csv_file_path, record):
    """
    Write a record to a CSV file.

    Parameters:
        csv_file_path (str): Path to the CSV file.
        record (dict): Dictionary of column names and values to write.
    """
    global model
    file_exists = os.path.isfile(csv_file_path)
    log.info(f"Checking if file exists: {csv_file_path} - Exists: {file_exists}")

    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            
            if not file_exists:
                writer.writeheader()  # Write header if the file is new
                log.info("CSV header written successfully.")

            writer.writerow(record)
            log.info(f"Record written successfully: {record}")

    except Exception as e:
        log.error(f"Error writing to CSV file '{csv_file_path}': {e}")

@app.route('/add_customer', methods=['POST'])
def add_customer():
    """
    API to add a new customer record to the database.

    """
    # Get JSON data from the request
    data = request.json

    # Validate required fields
    required_fields = ['CustomerID', 'Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400


    client_ip = request.remote_addr  # Get client's IP address
    log.info(f"API Accessed: /get_data_from_csv from IP: {client_ip}")
    record = {
    'CustomerID' : data['CustomerID'],
    'Gender' : data['Gender'],
    'SeniorCitizen' : data['SeniorCitizen'],
    'Partner' : data['Partner'],
    'Dependents' : data['Dependents'],
    'Tenure' : data['Tenure'],
    'PhoneService' : data['PhoneService'],
    'MultipleLines' : data['MultipleLines'],
    'InternetService' : data['InternetService'],
    'OnlineSecurity' : data['OnlineSecurity'],
    'OnlineBackup' : data['OnlineBackup'],
    'DeviceProtection' : data['DeviceProtection'],
    'TechSupport' : data['TechSupport'],
    'StreamingTV' : data['StreamingTV'],
    'StreamingMovies' : data['StreamingMovies'],
    'Contract' : data['Contract'],
    'PaperlessBilling' : data['PaperlessBilling'],
    'PaymentMethod' : data['PaymentMethod'],
    'MonthlyCharges' : data['MonthlyCharges'],
    'TotalCharges' : data['TotalCharges'],
    'Churn' : data['Churn']
    }
    print(record)
    # Insert the record into the CSV file (if provided)
    if csv_file_path:
        write_to_csv(csv_file_path, record)
        print(f"Record written to CSV file '{csv_file_path}' successfully. from IP: {client_ip}")

    # Insert the record
    status = db_setup.add_customer_record(data['CustomerID'],data['Gender'],data['SeniorCitizen'],data['Partner'],data['Dependents'],data['Tenure'],data['PhoneService'],data['MultipleLines'],data['InternetService'],data['OnlineSecurity'],data['OnlineBackup'],data['DeviceProtection'],data['TechSupport'],data['StreamingTV'],data['StreamingMovies'],data['Contract'],data['PaperlessBilling'],data['PaymentMethod'],data['MonthlyCharges'],data['TotalCharges'],data['Churn'])
    if status==True:
        log.info("Customer record added successfully: %s from IP: %s", record,client_ip)
        return jsonify({"message": "Customer record added successfully", "CustomerID": data['CustomerID']}), 201
    else:
        log.error("Failed to add customer record: %s from %s", record,client_ip)
        return jsonify({"error": "Failed to add customer record"}), 500

# API to fetch log files
@app.route('/get_data_from_csv', methods=['GET'])
def get_data_from_csv():
    """
    API to fetch log files and track request IP addresses.
    """
    client_ip = request.remote_addr  # Get client's IP address
    log.info(f"API Accessed: /get_data_from_csv from IP: {client_ip}")

    try:
        # Check if the log file exists
        if not os.path.exists(csv_file_path):
            log.warning(f"Log file not found. IP: {client_ip}")
            return jsonify({"error": "Log file not found"}), 404


        # Read CSV file
        df = pd.read_csv(csv_file_path)

        log.info(f"Log file successfully retrieved by {client_ip}")
        return jsonify(df.to_dict(orient="records"))  # Ensure it's a list of dicts

    except Exception as e:
        log.error(f"Error fetching log file: {e} | IP: {client_ip}")
        return jsonify({"error": str(e)}), 500
    
# API to fetch log files
@app.route('/get_data_from_database', methods=['GET'])
def get_data_from_database():
    """
    API to fetch data from the database and track request IP addresses.
    """
    client_ip = request.remote_addr  # Get client's IP address
    log.info(f"API Accessed: /get_data_from_database from IP: {client_ip}")

    try:
        # Fetch data from the database
        database_contents = db_setup.fetch_all_customers()

        if not database_contents:
            log.warning(f"No data found in the database. IP: {client_ip}")
            return jsonify({"message": "No data found"}), 404

        log.info(f"Database data successfully retrieved by {client_ip}")

        # Return the data as JSON
        return jsonify(database_contents), 200

    except Exception as e:
        log.error(f"Error fetching data from database: {e} | IP: {client_ip}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    global model
    model=model_initialize()
    app.run(host='0.0.0.0', port=5000,debug=True)
