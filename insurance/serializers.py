from rest_framework import serializers

from insurance.models import Policy, Quote, Customer


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'policy_type', 'age_multiplier', 'premium_to_cover_ratio']


class CustomerField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        if hasattr(self.context['request'].user, 'customer'):
            return Customer.objects.filter(id=self.context['request'].user.id)
        return Customer.objects.all()


class QuoteSerializer(serializers.ModelSerializer):
    customer = CustomerField()

    class Meta:
        model = Quote
        fields = ['id', 'customer', 'policy', 'cover', 'premium', 'status', 'valid_from', 'valid_to']
        read_only_fields = ['valid_to', 'valid_from', 'premium']


class QuoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['policy', 'total_premium']
