# import pandas as pd
# import numpy as np
# from faker import Faker

# # Initialize Faker for generating fake data
# fake = Faker()

# # Set random seed for reproducibility
# np.random.seed(42)

# # Number of rows in the dataset
# num_rows = 10000

# # Function to generate Web Logs Data
# def generate_web_logs_data(num_rows):
#     data = {
#         "User ID": [fake.uuid4() for _ in range(num_rows)],
#         "Session Duration (minutes)": np.random.randint(1, 60, num_rows),
#         "Page Views": np.random.randint(1, 20, num_rows),
#         "Browsing Behavior": np.random.choice(["Exploratory", "Focused", "Casual"], num_rows),
#         "Clickstream Data": [fake.text(max_nb_chars=50) for _ in range(num_rows)],
#         "Churn": np.random.choice(["Yes", "No"], num_rows)
#     }
#     return pd.DataFrame(data)

# # Key Data Sources:
# # 1. Transactional Data (CSV):
# # Attributes: CustomerID, TransactionDate, Amount, SubscriptionType, PaymentMethod,
# # etc.
# # Frequency: Daily or Weekly updates.
# # 2. Web Logs (API):
# # Attributes: CustomerID, Page Views, Session Duration, Time on Site, Clicks, etc.
# # Frequency: Hourly updates via an API.
# # i need csv add extra column Chunk [yes/no]
# # generate by using faker
# # Function to generate Transactional Data
# def generate_transactional_data(num_rows):
#     # data = {
#     #     "Customer ID": [fake.uuid4() for _ in range(num_rows)],
#     #     "Account Status": np.random.choice(["Active", "Canceled"], num_rows),
#     #     "Subscription Plan": np.random.choice(["Basic", "Premium", "Enterprise"], num_rows),
#     #     "Purchase History": np.random.randint(1, 100, num_rows),
#     #     "Payment Frequency": np.random.choice(["Monthly", "Quarterly", "Yearly"], num_rows),
#     #     "Churn": np.random.choice(["Yes", "No"], num_rows)
#     # }
#     # Generate synthetic transactional data
#     data = {
#         "CustomerID": [i for i in range(1,num_rows+1)],  # Unique customer ID
#         "TransactionDate": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_rows)],  # Random date within the last year
#         "Amount": np.random.randint(10, 500, num_rows),  # Random transaction amount between $10 and $500
#         "SubscriptionType": np.random.choice(["Basic", "Premium", "Enterprise"], num_rows),  # Random subscription type
#         "PaymentMethod": np.random.choice(["Credit Card", "Debit Card", "PayPal"], num_rows),  # Random payment method
#         "Churn": np.random.choice([0, 1], num_rows, p=[0.3, 0.7])  # Churn column with 30% "Yes" and 70% "No"
#     }

#     # Create a DataFrame
#     df = pd.DataFrame(data)
#     return df

# # Function to generate Third-party API Data
# def generate_third_party_data(num_rows):
#     data = {
#         "Customer ID": [fake.uuid4() for _ in range(num_rows)],
#         "Location": [fake.country() for _ in range(num_rows)],
#         "Income Level": np.random.choice(["Low", "Medium", "High"], num_rows),
#         "Social Media Sentiment": np.random.choice(["Positive", "Neutral", "Negative"], num_rows),
#         "Feedback Score": np.random.randint(1, 10, num_rows),
#         "External Service Usage": np.random.choice(["Yes", "No"], num_rows),
#         "Churn": np.random.choice(["Yes", "No"], num_rows)
#     }
#     return pd.DataFrame(data)

# # Function to generate Customer Service Data
# def generate_customer_service_data(num_rows):
#     data = {
#         "Customer ID": [fake.uuid4() for _ in range(num_rows)],
#         "Support Tickets": np.random.randint(0, 10, num_rows),
#         "Response Time (hours)": np.random.randint(1, 72, num_rows),
#         "Issue Resolution Time (days)": np.random.randint(1, 30, num_rows),
#         "Customer Satisfaction Score (NPS)": np.random.randint(0, 10, num_rows),
#         "Churn": np.random.choice(["Yes", "No"], num_rows)
#     }
#     return pd.DataFrame(data)

# # Function to generate Historical Churn Data
# def generate_historical_churn_data(num_rows):
#     data = {
#         "Customer ID": [fake.uuid4() for _ in range(num_rows)],
#         "Churn Status": np.random.choice([0, 1], num_rows, p=[0.7, 0.3]),  # 30% churn rate
#         "Date of Churn": [fake.date_between(start_date="-1y", end_date="today") for _ in range(num_rows)],
#         "Reason for Churn": np.random.choice(["Price", "Service", "Product", "Unknown"], num_rows),
#         "Churn": np.random.choice(["Yes", "No"], num_rows)
#     }
#     return pd.DataFrame(data)

# # Generate datasets
# web_logs_data = generate_web_logs_data(num_rows)
# transactional_data = generate_transactional_data(num_rows)
# # third_party_data = generate_third_party_data(num_rows)
# # customer_service_data = generate_customer_service_data(num_rows)
# # historical_churn_data = generate_historical_churn_data(num_rows)

# # Save datasets to CSV files
# web_logs_data.to_csv("web_logs_data.csv", index=False)
# transactional_data.to_csv("transactional_data.csv", index=False)
# # third_party_data.to_csv("third_party_data.csv", index=False)
# # customer_service_data.to_csv("customer_service_data.csv", index=False)
# # historical_churn_data.to_csv("historical_churn_data.csv", index=False)

# print("Datasets generated and saved to CSV files.")

import pandas as pd

# Read CSV file
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Convert DataFrame to JSON
json_data = df.to_json(orient="records", indent=4)

# Save JSON to file
with open("output.json", "w") as json_file:
    json_file.write(json_data)

print("CSV successfully converted to JSON!")
