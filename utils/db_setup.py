from sqlalchemy import create_engine, Column, Integer, String, DateTime,inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# from constants import csv_file_path
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
# Define paths relative to the project root
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the project root directory
DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR, "db", "database.db")}'  # Path to the database
csv_file_path = os.path.join(BASE_DIR, "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")  # Path to the CSV file
engine = create_engine(DATABASE_URL, echo=False)
import pandas as pd
# Base class for SQLAlchemy models
Base = declarative_base()

class customer(Base):
    __tablename__ = 'customer_service'

    CustomerID = Column(Integer, primary_key=True)  # String ID
    Gender = Column(String(10), nullable=False)
    SeniorCitizen = Column(Integer)  # 0 or 1
    Partner = Column(String(5))  # Yes/No -> String(5)
    Dependents = Column(String(5))
    Tenure = Column(Integer)  # Months
    PhoneService = Column(String(5))
    MultipleLines = Column(String(50))  # "No phone service", "Yes", "No"
    InternetService = Column(String(50))  # "DSL", "Fiber optic", "No"
    OnlineSecurity = Column(String(50))
    OnlineBackup = Column(String(50))
    DeviceProtection = Column(String(50))
    TechSupport = Column(String(50))
    StreamingTV = Column(String(50))
    StreamingMovies = Column(String(50))
    Contract = Column(String(50))  # "Month-to-month", "One year", "Two year"
    PaperlessBilling = Column(String(5))  # Yes/No
    PaymentMethod = Column(String(50))  # "Electronic check", "Mailed check", etc.
    MonthlyCharges = Column(Float)  # Numeric
    TotalCharges = Column(Float)  # Numeric
    Churn = Column(String(5))  # Yes/No -> String(5)


# Create all tables
Base.metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(bind=engine)


def add_customer_record(CustomerID ,Gender ,SeniorCitizen ,Partner ,Dependents ,Tenure ,PhoneService ,MultipleLines ,InternetService ,OnlineSecurity ,OnlineBackup ,DeviceProtection ,TechSupport ,StreamingTV ,StreamingMovies ,Contract ,PaperlessBilling ,PaymentMethod ,MonthlyCharges ,TotalCharges ,Churn):
    """
    Add a customer to the database, avoiding duplicates.
    """
    session = SessionLocal()
    try:
        # Check if the customername already exists
        # existing_customer = session.query(customer).filter_by(CustomerID=CustomerID).first()
        # if existing_customer:
        #     print(f"customer '{CustomerID}' already exists. Skipping insertion.")
        #     return False

        # Hash the password and insert the new customer
        new_customer = customer(
            CustomerID =CustomerID,
            Gender =Gender ,
            SeniorCitizen =SeniorCitizen ,
            Partner =Partner ,
            Dependents =Dependents ,
            Tenure =Tenure ,
            PhoneService =PhoneService,
            MultipleLines =MultipleLines,
            InternetService =InternetService,
            OnlineSecurity =OnlineSecurity,
            OnlineBackup =OnlineBackup,
            DeviceProtection =DeviceProtection,
            TechSupport =TechSupport,
            StreamingTV =StreamingTV,
            StreamingMovies =StreamingMovies,
            Contract =Contract,
            PaperlessBilling =PaperlessBilling,
            PaymentMethod =PaymentMethod,
            MonthlyCharges =MonthlyCharges,
            TotalCharges =TotalCharges,
            Churn =Churn
        )
        session.add(new_customer)
        session.commit()
        print(f"customer '{CustomerID}' added successfully.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error adding customer '{CustomerID}': {e}")
        return False
    finally:
        session.close()



# Fetch all customers
def fetch_all_customers():
    session = SessionLocal()
    print(True)
    try:
        customers_records=session.query(customer).all()
        # print(customers_records)
        '''
        TotalSpend = Column(Float)  # Aggregated Feature
    ActivityFrequency = Column(Integer)  # Derived Feature'''
        return ([[customer.CustomerID ,customer.Gender ,customer.SeniorCitizen ,customer.Partner ,customer.Dependents ,customer.Tenure ,customer.PhoneService ,customer.MultipleLines ,customer.InternetService ,customer.OnlineSecurity ,customer.OnlineBackup ,customer.DeviceProtection ,customer.TechSupport ,customer.StreamingTV ,customer.StreamingMovies ,customer.Contract ,customer.PaperlessBilling ,customer.PaymentMethod ,customer.MonthlyCharges ,customer.TotalCharges ,customer.Churn]for customer in customers_records])
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        print("Database error:", str(e))
    finally:
        session.close()

# Fetch customers by parameter
def fetch_customers_by_parameter(**kwargs):
    session = SessionLocal()
    try:
        customer_record=session.query(customer).filter_by(**kwargs).all()
        return [[customer.CustomerID ,customer.Gender ,customer.SeniorCitizen ,customer.Partner ,customer.Dependents ,customer.Tenure ,customer.PhoneService ,customer.MultipleLines ,customer.InternetService ,customer.OnlineSecurity ,customer.OnlineBackup ,customer.DeviceProtection ,customer.TechSupport ,customer.StreamingTV ,customer.StreamingMovies ,customer.Contract ,customer.PaperlessBilling ,customer.PaymentMethod ,customer.MonthlyCharges ,customer.TotalCharges ,customer.Churn] for customer in customer_record]
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        print("Database error:", str(e))
    finally:
        session.close()

# Update customer parameters
def update_customer(CustomerID, updates=None, **kwargs):
    session = SessionLocal()
    try:
        Customer = session.query(customer).filter(customer.CustomerID == CustomerID).first()
        if Customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
                print("!!!!!!!!!!!!!!!!!!!!1",kwargs)
            session.commit()
            # session.refresh(customer)
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        print("Database error:", str(e))
    finally:
        session.close()

# Delete customer by parameter
def delete_customer_by_parameter(**kwargs):
    session = SessionLocal()
    try:
        customers_to_delete = session.query(customer).filter_by(**kwargs).all()
        for customer_ in customers_to_delete:
            session.delete(customer_)
        session.commit()
        return len(customers_to_delete) > 0
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error
        print("Database error:", str(e))
    finally:
        session.close()


def delete_table(table_class):

    if inspect(engine).has_table(table_class.__tablename__):
        session = SessionLocal()
        try:
            table_class.__table__.drop(engine)
            print(f"Table '{table_class.__tablename__}' deleted.")
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()  # Rollback in case of error
            print("Database error:", str(e))
    else:
        print(f"Table '{table_class.__tablename__}' does not exist.")


# Example usage
if __name__ == "__main__":
    # delete_table(customer)
    # # Add a customer
    # add_customer_record(1, '2024-10-08', '146', 'Enterprise', 'Debit Card', '1')

    # # # Fetch all customers
    print(fetch_all_customers())

    # # # Fetch customers by parameter
    # print(fetch_customers_by_parameter(CustomerID="1"))

    # # # Update customer details

    # update_customer(CustomerID="1", Churn=1)

    # Delete a customer
    # delete_customer_by_parameter(CustomerID="1")
    # with open(csv_file_path,'r') as f:
    #     for line in f.readlines()[1::]:
    #         print(line[:-1:].split(','))
    #         # if int(line[:-1:].split(',')[0])<:
    #         #     continue
    #         add_customer_record(*line[:-1:].split(','))
    ...

