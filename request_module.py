import requests
import json
from datetime import datetime

# Base URL of the API
BASE_URL = "http://localhost:5000"  # Replace with your API's base URL

def predict_churn(CustomerID,Gender,SeniorCitizen,Partner,Dependents,Tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges):
    """
    Make a churn prediction via the /predict API.

    Parameters:
        amount (float): Amount of the transaction.
        subscription_type (str): Type of subscription (e.g., "Basic", "Premium").
        payment_method (str): Payment method (e.g., "Credit Card", "PayPal").

    Returns:
        dict: Response from the API.
    """
    url = f"{BASE_URL}/predict"
    payload = {
        "CustomerID":CustomerID,
        "Gender":Gender,
        "SeniorCitizen":SeniorCitizen,
        "Partner":Partner,
        "Dependents":Dependents,
        "Tenure":Tenure,
        "PhoneService":PhoneService,
        "MultipleLines":MultipleLines,
        "InternetService":InternetService,
        "OnlineSecurity":OnlineSecurity,
        "OnlineBackup":OnlineBackup,
        "DeviceProtection":DeviceProtection,
        "TechSupport":TechSupport,
        "StreamingTV":StreamingTV,
        "StreamingMovies":StreamingMovies,
        "Contract":Contract,
        "PaperlessBilling":PaperlessBilling,
        "PaymentMethod":PaymentMethod,
        "MonthlyCharges":MonthlyCharges,
        "TotalCharges":TotalCharges,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_logs():
    """
    Fetch logs via the /get_logs API.

    Returns:
        dict: Response from the API.
    """
    url = f"{BASE_URL}/get_logs"

    try:
        response = requests.get(url)
        print(response.text)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def add_customer(CustomerID,Gender,SeniorCitizen,Partner,Dependents,Tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges,Churn):
    """
    Add a new customer record via the /add_customer API.

    Parameters:
        customer_id (int): Customer ID.
        transaction_date (str): Transaction date in 'YYYY-MM-DD' format.
        amount (float): Transaction amount.
        subscription_type (str): Type of subscription.
        payment_method (str): Payment method.
        churn (int): Churn status (0 or 1).

    Returns:
        dict: Response from the API.
    """
    url = f"{BASE_URL}/add_customer"
    payload = {
        "CustomerID":CustomerID,
        "Gender":Gender,
        "SeniorCitizen":SeniorCitizen,
        "Partner":Partner,
        "Dependents":Dependents,
        "Tenure":Tenure,
        "PhoneService":PhoneService,
        "MultipleLines":MultipleLines,
        "InternetService":InternetService,
        "OnlineSecurity":OnlineSecurity,
        "OnlineBackup":OnlineBackup,
        "DeviceProtection":DeviceProtection,
        "TechSupport":TechSupport,
        "StreamingTV":StreamingTV,
        "StreamingMovies":StreamingMovies,
        "Contract":Contract,
        "PaperlessBilling":PaperlessBilling,
        "PaymentMethod":PaymentMethod,
        "MonthlyCharges":MonthlyCharges,
        "TotalCharges":TotalCharges,
        "Churn": Churn
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
if __name__=="__main__":

    # # Example: Make a churn prediction
    prediction_response = predict_churn(CustomerID="7590-VHVEG",Gender='Female',SeniorCitizen=0,Partner='Yes',Dependents='No',Tenure=1,PhoneService='No',MultipleLines='No phone service',InternetService='DSL',OnlineSecurity='No',OnlineBackup='Yes',DeviceProtection='No',TechSupport='No',StreamingTV='No',StreamingMovies='No',Contract='Month-to-month',PaperlessBilling='Yes',PaymentMethod='Electronic check',MonthlyCharges=29.85,TotalCharges=29.85)
    print("Churn Prediction Response:", prediction_response)

    # # Example: Fetch logs
    # logs_response = get_logs()
    # print("Logs Response:", logs_response)

    # # Example: Add a new customer record
#     customer_response = add_customer(
#         CustomerID='7590-VHVEM',
# Gender='Female',
# SeniorCitizen=0,
# Partner='Yes',
# Dependents='No',
# Tenure=1,
# PhoneService='No',
# MultipleLines='No phone service',
# InternetService='DSL',
# OnlineSecurity='No',
# OnlineBackup='Yes',
# DeviceProtection='No',
# TechSupport='No',
# StreamingTV='No',
# StreamingMovies='No',
# Contract='Month-to-month',
# PaperlessBilling='Yes',
# PaymentMethod='Electronic check',
# MonthlyCharges=29.85,
# TotalCharges=29.85,
# Churn='No'
#     )
#     print("Add Customer Response:", customer_response)
