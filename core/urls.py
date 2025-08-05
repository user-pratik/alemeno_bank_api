# from django.urls import path
# from .views import (
#     CustomerListCreateView,
#     LoanListCreateView,
#     RegisterCustomerView,
#     CheckEligibilityView,
# )

# urlpatterns = [
#     path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
#     path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
#     path('register/', RegisterCustomerView.as_view(), name='register-customer'),
#     path('check-eligibility/', CheckEligibilityView.as_view(), name='check-eligibility'),
# ]
from django.urls import path
from .views import (
    CustomerListCreateView,
    LoanListCreateView,
    RegisterCustomerView,
    CheckEligibilityView,
    CreateLoanView,
    ViewLoanDetailView,
    ViewLoansByCustomerView,
)

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('register/', RegisterCustomerView.as_view(), name='register-customer'),
    path('check-eligibility/', CheckEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan/', CreateLoanView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>/', ViewLoanDetailView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>/', ViewLoansByCustomerView.as_view(), name='view-loans'),
]
