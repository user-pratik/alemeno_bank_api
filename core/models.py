from django.db import models

class Customer(models.Model):
    # customer_id = models.IntegerField(unique=True, default=0)  # Customer ID from file
    customer_id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=100, default='Unknown')
    last_name = models.CharField(max_length=100, default='Unknown')
    age = models.IntegerField(default=30)
    phone_number = models.CharField(max_length=20, default='0000000000')
    monthly_salary = models.BigIntegerField(default=0)
    approved_limit = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    # loan_id = models.IntegerField(unique=True, default=0)
    loan_id = models.AutoField(primary_key=True)

    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tenure = models.IntegerField(default=0)  # months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # annual %
    monthly_repayment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer}"
