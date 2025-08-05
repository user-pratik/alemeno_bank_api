# from rest_framework import generics
# from rest_framework.generics import GenericAPIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.utils import timezone
# from .models import Customer, Loan
# from .serializers import (
#     CustomerSerializer,
#     LoanSerializer,
#     RegisterCustomerSerializer,
#     CheckEligibilitySerializer,
# )


# def calculate_emi(principal, annual_interest_rate, tenure_months):
#     r = annual_interest_rate / (12 * 100)
#     n = tenure_months
#     if r == 0:
#         return round(principal / n, 2)
#     emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
#     return round(emi, 2)


# class RegisterCustomerView(generics.CreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = RegisterCustomerSerializer


# class CustomerListCreateView(generics.ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer


# class LoanListCreateView(generics.ListCreateAPIView):
#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer


# class CheckEligibilityView(GenericAPIView):
#     serializer_class = CheckEligibilitySerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data

#         customer_id = data['customer_id']
#         loan_amount = data['loan_amount']
#         interest_rate = data['interest_rate']
#         tenure = data['tenure']

#         try:
#             customer = Customer.objects.get(customer_id=customer_id)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

#         all_loans = Loan.objects.filter(customer=customer)
#         today = timezone.now().date()
#         current_loans = all_loans.filter(end_date__gte=today)

#         # If current loans sum > approved limit → credit_score = 0
#         current_loan_sum = sum(float(loan.loan_amount) for loan in current_loans)
#         if current_loan_sum > customer.approved_limit:
#             credit_score = 0
#         else:
#             total_loans = all_loans.count()
#             if total_loans > 0:
#                 total_emis = sum(loan.tenure for loan in all_loans)
#                 emis_paid_on_time = sum(loan.emis_paid_on_time for loan in all_loans)
#                 score_paid_on_time = min(20, (emis_paid_on_time / total_emis) * 20) if total_emis > 0 else 10
#             else:
#                 score_paid_on_time = 10

#             score_num_loans = min(20, (total_loans / 5) * 20)

#             loans_this_year = all_loans.filter(start_date__year=today.year).count()
#             score_activity = min(20, (loans_this_year / 3) * 20)

#             total_loan_volume = sum(float(loan.loan_amount) for loan in all_loans)
#             max_vol = customer.approved_limit * 5 if customer.approved_limit > 0 else 1
#             score_volume = max(0, 20 - ((total_loan_volume / max_vol) * 20))
#             score_volume = min(20, score_volume)

#             credit_score = score_paid_on_time + score_num_loans + score_activity + score_volume
#             credit_score = min(100, credit_score)

#         current_emi_sum = sum(float(loan.monthly_repayment) for loan in current_loans)
#         if current_emi_sum > 0.5 * customer.monthly_salary:
#             approval = False
#         else:
#             approval = False
#             if credit_score > 50:
#                 approval = True
#             elif 30 < credit_score <= 50:
#                 approval = interest_rate > 12
#             elif 10 < credit_score <= 30:
#                 approval = interest_rate > 16

#         corrected_interest_rate = interest_rate
#         if credit_score > 50:
#             pass
#         elif 30 < credit_score <= 50 and interest_rate <= 12:
#             corrected_interest_rate = 16
#         elif 10 < credit_score <= 30 and interest_rate <= 16:
#             corrected_interest_rate = 16

#         monthly_installment = calculate_emi(loan_amount, corrected_interest_rate, tenure)

#         response_data = {
#             "customer_id": customer.customer_id,
#             "approval": approval,
#             "interest_rate": interest_rate,
#             "corrected_interest_rate": corrected_interest_rate,
#             "tenure": tenure,
#             "monthly_installment": monthly_installment
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
from rest_framework import generics
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Customer, Loan
from .serializers import (
    CustomerSerializer,
    LoanSerializer,
    RegisterCustomerSerializer,
    CheckEligibilitySerializer,
    CreateLoanSerializer,
    CreateLoanResponseSerializer,
    ViewLoanSerializer,
    ViewLoansByCustomerSerializer,
)


def calculate_emi(principal, annual_interest_rate, tenure_months):
    r = annual_interest_rate / (12 * 100)
    n = tenure_months
    if r == 0:
        return round(principal / n, 2)
    emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    return round(emi, 2)


class RegisterCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterCustomerSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CheckEligibilityView(GenericAPIView):
    serializer_class = CheckEligibilitySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer_id = data['customer_id']
        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        all_loans = Loan.objects.filter(customer=customer)
        today = timezone.now().date()
        current_loans = all_loans.filter(end_date__gte=today)

        current_loan_sum = sum(float(loan.loan_amount) for loan in current_loans)
        if current_loan_sum > customer.approved_limit:
            credit_score = 0
        else:
            total_loans = all_loans.count()
            if total_loans > 0:
                total_emis = sum(loan.tenure for loan in all_loans)
                emis_paid_on_time = sum(loan.emis_paid_on_time for loan in all_loans)
                score_paid_on_time = min(20, (emis_paid_on_time / total_emis) * 20) if total_emis > 0 else 10
            else:
                score_paid_on_time = 10

            score_num_loans = min(20, (total_loans / 5) * 20)

            loans_this_year = all_loans.filter(start_date__year=today.year).count()
            score_activity = min(20, (loans_this_year / 3) * 20)

            total_loan_volume = sum(float(loan.loan_amount) for loan in all_loans)
            max_vol = customer.approved_limit * 5 if customer.approved_limit > 0 else 1
            score_volume = max(0, 20 - ((total_loan_volume / max_vol) * 20))
            score_volume = min(20, score_volume)

            credit_score = score_paid_on_time + score_num_loans + score_activity + score_volume
            credit_score = min(100, credit_score)

        current_emi_sum = sum(float(loan.monthly_repayment) for loan in current_loans)
        if current_emi_sum > 0.5 * customer.monthly_salary:
            approval = False
        else:
            approval = False
            if credit_score > 50:
                approval = True
            elif 30 < credit_score <= 50:
                approval = interest_rate > 12
            elif 10 < credit_score <= 30:
                approval = interest_rate > 16

        corrected_interest_rate = interest_rate
        if credit_score > 50:
            pass
        elif 30 < credit_score <= 50 and interest_rate <= 12:
            corrected_interest_rate = 16
        elif 10 < credit_score <= 30 and interest_rate <= 16:
            corrected_interest_rate = 16

        monthly_installment = calculate_emi(loan_amount, corrected_interest_rate, tenure)

        response_data = {
            "customer_id": customer.customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": monthly_installment
        }
        return Response(response_data, status=status.HTTP_200_OK)


class CreateLoanView(GenericAPIView):
    serializer_class = CreateLoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer_id = data['customer_id']
        loan_amount = data['loan_amount']
        interest_rate = data['interest_rate']
        tenure = data['tenure']

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # eligibility check logic (reuse CheckEligibilityView logic ideally, simplified here)
        all_loans = Loan.objects.filter(customer=customer)
        today = timezone.now().date()
        current_loans = all_loans.filter(end_date__gte=today)

        current_loan_sum = sum(float(loan.loan_amount) for loan in current_loans)
        if current_loan_sum > customer.approved_limit:
            approved = False
            message = "Loan not approved: current loans exceed approved limit."
        else:
            current_emi_sum = sum(float(loan.monthly_repayment) for loan in current_loans)
            if current_emi_sum > 0.5 * customer.monthly_salary:
                approved = False
                message = "Loan not approved: outstanding EMIs exceed 50% monthly salary."
            else:
                approved = True
                message = "Loan approved."

        if not approved:
            monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": message,
                "monthly_installment": monthly_installment,
            }, status=status.HTTP_200_OK)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure=tenure,
            monthly_repayment=calculate_emi(loan_amount, interest_rate, tenure),
            emis_paid_on_time=0,
            start_date=today,
            end_date=today.replace(year=today.year + tenure // 12 + (1 if tenure % 12 > 0 else 0))
        )
        monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved and created successfully.",
            "monthly_installment": monthly_installment,
        }, status=status.HTTP_201_CREATED)


class ViewLoanDetailView(RetrieveAPIView):
    serializer_class = ViewLoanSerializer
    lookup_field = 'loan_id'
    queryset = Loan.objects.all()


class ViewLoansByCustomerView(ListAPIView):
    serializer_class = ViewLoansByCustomerSerializer

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        today = timezone.now().date()
        return Loan.objects.filter(customer__customer_id=customer_id, end_date__gte=today)
