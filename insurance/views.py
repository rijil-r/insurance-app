import django_filters
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from insurance.models import Policy, Customer, Quote
from insurance.permissions import AdminPermission
from insurance.serializers import PolicySerializer, CustomerCreateSerializer, QuoteSerializer


class PolicyFilter(django_filters.FilterSet):
    customer = django_filters.NumberFilter(field_name='quote__customer')

    class Meta:
        model = Policy
        fields = ['customer']


# Create your views here.
class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [AdminPermission]
    filterset_class = PolicyFilter

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        # get status and filter based on that
        if request.query_params.get('status'):
            quotes = Quote.objects.filter(policy=pk, status=request.query_params.get('status'))
        else:
            quotes = Quote.objects.filter(policy=pk)
        return Response(QuoteSerializer(quotes, many=True).data)


class CustomerCreateView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
    permission_classes = [AdminPermission]

    def perform_create(self, serializer, password):
        serializer.save(password=make_password(password))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = Customer.objects.make_random_password()
        self.perform_create(serializer, password)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['password'] = password
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    filterset_fields = ['status']

    def get_queryset(self):
        if hasattr(self.request.user, 'customer'):
            return Quote.objects.filter(customer=self.request.user.customer)
        return Quote.objects.all()
