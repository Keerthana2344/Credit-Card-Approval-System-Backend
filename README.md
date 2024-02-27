# Credit-Card-Approval-System-Backend
For this assignment, we will create a credit approval system using Python/Django and PostgreSQL. We will use Django Rest Framework (DRF) for the API and Celery for background tasks.
First, let's set up the project and install the necessary dependencies:

$ django-admin startproject credit_approval_system
$ cd credit_approval_system
$ pip install -r requirements.txt

Then, create a new app called "credit":
$ python manage.py startapp credit

Now, let's create the necessary data models in "credit/models.py":

from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

Next, we will create serializers for the models in "credit/serializers.py":


from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

Now, let's create the views for the models in "credit/views.py":


from rest_framework import viewsets
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

Finally, let's create the API endpoints in "credit/urls.py":

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

Now, let's create a Celery task to ingest the data from the provided Excel files:


from celery import shared_task
from .models import Customer, Loan
from .utils import load_customer_data, load_loan_data


def ingest_data():
    load_customer_data('customer_data.xlsx')
    load_loan_data('loan_data.xlsx')
In "credit/utils.py", we will define the functions to load the data from the Excel files:


import pandas as pd
from .models import Customer, Loan

def load_customer_data(file_name):
    df = pd.read_excel(file_name)
    for _, row in df.iterrows

