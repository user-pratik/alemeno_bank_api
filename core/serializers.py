
from rest_framework import serializers
from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    monthly_installment = serializers.FloatField(source='monthly_repayment')

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer_name', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure']

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"



class RegisterCustomerSerializer(serializers.ModelSerializer):
    monthly_income = serializers.IntegerField(source='monthly_salary')
    name = serializers.SerializerMethodField()
    approved_limit = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'first_name',
            'last_name',
            'name',
            'age',
            'monthly_income',
            'approved_limit',
            'phone_number'
        ]
        read_only_fields = ['customer_id', 'approved_limit', 'name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def to_representation(self, instance):
        """Is method ko override kar ke response se first_name aur last_name hataenge"""
        rep = super().to_representation(instance)
        rep.pop('first_name', None)
        rep.pop('last_name', None)
        return rep

    def create(self, validated_data):
        monthly_salary = validated_data.pop('monthly_salary')
        approved_limit = round((36 * monthly_salary) / 100000) * 100000
        customer = Customer.objects.create(
            monthly_salary=monthly_salary,
            approved_limit=approved_limit,
            **validated_data
        )
        return customer


class CheckEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(label="Customer ID")
    loan_amount = serializers.FloatField(label="Requested Loan Amount")
    interest_rate = serializers.FloatField(label="Interest Rate (%)")
    tenure = serializers.IntegerField(label="Tenure (months)")


class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(label="Customer ID")
    loan_amount = serializers.FloatField(label="Requested Loan Amount")
    interest_rate = serializers.FloatField(label="Interest Rate (%)")
    tenure = serializers.IntegerField(label="Tenure (months)")


class CreateLoanResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()
    monthly_installment = serializers.FloatField()


class ViewLoanSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    monthly_installment = serializers.FloatField(source='monthly_repayment')

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure']

    def get_customer(self, obj):
        return {
            'id': obj.customer.customer_id,
            'first_name': obj.customer.first_name,
            'last_name': obj.customer.last_name,
            'phone_number': obj.customer.phone_number,
            'age': obj.customer.age,
        }


class ViewLoansByCustomerSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.FloatField(source='monthly_repayment')
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'repayments_left']

    def get_repayments_left(self, obj):
        left = max(obj.tenure - obj.emis_paid_on_time, 0)
        return left
