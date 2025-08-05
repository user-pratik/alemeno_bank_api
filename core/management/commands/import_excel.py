from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Customer, Loan
import os

class Command(BaseCommand):
    help = "Imports customer and loan data from Excel files located in project root."

    def add_arguments(self, parser):
        # Default paths relative to project root (manage.py ke folder se)
        parser.add_argument('--customer_file', type=str, default='customer_data.xlsx')
        parser.add_argument('--loan_file', type=str, default='loan_data.xlsx')

    def handle(self, *args, **options):
        # Excel file paths relative to current working directory
        customer_file = options['customer_file']
        loan_file = options['loan_file']

        self.stdout.write(self.style.NOTICE(f'Importing customers from {customer_file}'))
        df_cust = pd.read_excel(customer_file, engine='openpyxl')
        for _, row in df_cust.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row.get('Age', 0),
                    'phone_number': str(row['Phone Number']),
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Customer import complete!'))

        self.stdout.write(self.style.NOTICE(f'Importing loans from {loan_file}'))
        df_loan = pd.read_excel(loan_file, engine='openpyxl')
        for _, row in df_loan.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['Customer ID'])
            except Customer.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Skipped loan_id={row["Loan ID"]}: customer_id={row["Customer ID"]} NOT FOUND.'))
                continue
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_repayment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': pd.to_datetime(row['Date of Approval']).date(),
                    'end_date': pd.to_datetime(row['End Date']).date(),
                }
            )
        self.stdout.write(self.style.SUCCESS('Loan import complete!'))
