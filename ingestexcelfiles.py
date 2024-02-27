from celery import shared_task
from .models import Customer, Loan
from .utils import load_customer_data, load_loan_data

@shared_task
def ingest_data():
    load_customer_data('customer_data.xlsx')
    load_loan_data('loan_data.xlsx')