from rest_framework.routers import DefaultRouter

from insurance.views import PolicyViewSet, CustomerCreateView, QuoteViewSet

router = DefaultRouter()

router.register(r'policies', PolicyViewSet, basename='policy')
router.register(r'create_customers', CustomerCreateView, basename='create-customer')
router.register(r'quotes', QuoteViewSet, basename='quote')

url_patterns = router.urls
