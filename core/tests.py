from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Customer, Loan
from .serializers import RegisterCustomerSerializer
from django.utils import timezone

class CustomerModelTests(TestCase):
    def test_customer_str(self):
        customer = Customer.objects.create(
            customer_id=99,
            first_name="Test",
            last_name="Model",
            age=31,
            phone_number="9191919191",
            monthly_salary=55000,
            approved_limit=2000000
        )
        self.assertEqual(str(customer), "Test Model")

class LoanModelTests(TestCase):
    def test_loan_str(self):
        customer = Customer.objects.create(
            customer_id=80,
            first_name="Loan",
            last_name="Customer",
            age=40,
            phone_number="8800880088",
            monthly_salary=87000,
            approved_limit=2500000
        )
        loan = Loan.objects.create(
            customer=customer,
            loan_id=89,
            loan_amount=100000,
            tenure=12,
            interest_rate=10,
            monthly_repayment=9000,
            emis_paid_on_time=10,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        self.assertTrue(str(loan).startswith("Loan"))

class RegisterCustomerSerializerTests(TestCase):
    def test_register_customer_serializer_creates_customer(self):
        data = {
            "first_name": "Seri",
            "last_name": "Alizer",
            "age": 22,
            "monthly_income": 50000,
            "phone_number": "1234509876"
        }
        serializer = RegisterCustomerSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        customer = serializer.save()
        self.assertTrue(customer.customer_id)
        self.assertEqual(customer.approved_limit, 1800000)  # 36*50000 = 18,00,000 (nearest lakh)

class RegisterCustomerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_customer(self):
        payload = {
            "first_name": "API",
            "last_name": "Tester",
            "age": 25,
            "monthly_income": 40000,
            "phone_number": "7777777777"
        }
        url = reverse("register-customer")
        resp = self.client.post(url, data=payload, format='json')
        self.assertIn(resp.status_code, [200, 201])
        # self.assertEqual(resp.data["first_name"], "API")
        self.assertEqual(resp.data["name"], "API Tester")
        self.assertNotIn("first_name", resp.data)
        self.assertNotIn("last_name", resp.data)
        self.assertEqual(resp.data["monthly_income"], 40000)
        self.assertEqual(resp.data["approved_limit"], 1400000)  # 1,400,000 is correct
  # 36*40000

    def test_check_eligibility(self):
        # Create customer
        customer = Customer.objects.create(
            customer_id=23456,
            first_name="Elig",
            last_name="Test",
            age=30,
            phone_number="9876512345",
            monthly_salary=120000,
            approved_limit=4300000
        )
        url = reverse("check-eligibility")
        data = {
            "customer_id": customer.customer_id,
            "loan_amount": 500000,
            "interest_rate": 13,
            "tenure": 12
        }
        resp = self.client.post(url, data=data, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("approval", resp.data)
        self.assertIn("monthly_installment", resp.data)

    def test_create_loan_and_view_loan(self):
        # Setup test customer
        customer = Customer.objects.create(
            customer_id=22222,
            first_name="LoanAPI",
            last_name="User",
            age=33,
            phone_number="6666666666",
            monthly_salary=90000,
            approved_limit=3200000
        )
        # Test create-loan
        url_create = reverse("create-loan")
        payload = {
            "customer_id": customer.customer_id,
            "loan_amount": 200000,
            "interest_rate": 14,
            "tenure": 24
        }
        resp = self.client.post(url_create, data=payload, format='json')
        self.assertIn(resp.status_code, [200, 201])
        self.assertTrue(resp.data.get("loan_approved", False))
        loan_id = resp.data["loan_id"]

        # Test view-loan
        url_view = reverse("view-loan", kwargs={"loan_id": loan_id})
        resp2 = self.client.get(url_view)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.data["loan_id"], loan_id)
        self.assertEqual(resp2.data["customer"]["id"], customer.customer_id)

    def test_view_loans_by_customer(self):
        customer = Customer.objects.create(
            customer_id=12321,
            first_name="LoanBatch",
            last_name="User",
            age=28,
            phone_number="9988776655",
            monthly_salary=60000,
            approved_limit=2200000
        )
        Loan.objects.create(
            customer=customer,
            loan_id=110,
            loan_amount=100000,
            tenure=12,
            interest_rate=12,
            monthly_repayment=9000,
            emis_paid_on_time=10,
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        url = reverse("view-loans", kwargs={"customer_id": customer.customer_id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.data, list))
        if resp.data:
            item = resp.data[0]
            self.assertIn("repayments_left", item)
