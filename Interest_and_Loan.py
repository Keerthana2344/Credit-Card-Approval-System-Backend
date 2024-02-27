import pandas as pd
import json

class LoanManagementSystem:
    def __init__(self):
        self.loan_data = pd.read_excel('loan_data.xlsx')
        self.loan_data['approved_limit'] = self.loan_data['loan_amount'] * 0.5
        self.loan_data['interest_rate'] = self.calculate_interest_rate(self.loan_data['credit_score'])
        self.loan_data['tenure'] = self.calculate_tenure(self.loan_data['loan_amount'])
        self.loan_data['monthly_installment'] = self.calculate_monthly_installment(self.loan_data['loan_amount'], self.loan_data['interest_rate'], self.loan_data['tenure'])
        self.loan_data['approval'] = self.check_loan_eligibility(self.loan_data['credit_score'], self.loan_data['loan_amount'], self.loan_data['approved_limit'], self.loan_data['monthly_installment'])
        self.loan_data['corrected_interest_rate'] = self.loan_data['interest_rate']
        self.loan_data = self.loan_data.drop(columns=['loan_amount', 'interest_rate', 'tenure', 'monthly_installment'])
        self.loan_data = self.loan_data.rename(columns={'customer_id': 'id', 'approval': 'loan_approved', 'interest_rate': 'interest_rate', 'tenure': 'tenure', 'monthly_installment': 'monthly_installment'})
        self.loan_data['message'] = self.loan_data.apply(lambda row: 'Loan approved' if row['loan_approved'] else 'Loan not approved', axis=1)
        self.loan_data = self.loan_data.drop(columns=['approval'])

    def calculate_interest_rate(self, credit_score):
        if credit_score > 50:
            return 12
        elif 50 > credit_score > 30:
            return 16
        elif 30 > credit_score > 10:
            return 20
        else:
            return 24

    def calculate_tenure(self, loan_amount):
        return int(loan_amount / 1000) + 1

    def calculate_monthly_installment(self, loan_amount, interest_rate, tenure):
        monthly_interest_rate = interest_rate / (12 * 100)
        monthly_installment = loan_amount * (monthly_interest_rate * pow((1 + monthly_interest_rate), tenure)) / (pow((1 + monthly_interest_rate), tenure) - 1)
        return monthly_installment

    def check_loan_eligibility(self, credit_score, loan_amount, approved_limit, monthly_installment):
        if credit_score == 0:
            return False
        elif loan_amount > approved_limit:
            return False
        elif self.loan_data[self.loan_data['customer_id'] == customer_id]['monthly_installment'].sum() > 0.5 * monthly_income:
            return False
        else:
            return True

    def create_loan(self, customer_id, loan_amount, interest_rate, tenure):
        if self.check_loan_eligibility(self.loan_data[self.loan_data['customer_id'] == customer_id]['credit_score'].values[0], loan_amount, self.loan_data[self.loan_data['customer_id'] == customer_id]['approved_limit'].values[0], self.calculate_monthly_installment(loan_amount, interest_rate, tenure)):
            loan_id = self.loan_data.shape[0] + 1