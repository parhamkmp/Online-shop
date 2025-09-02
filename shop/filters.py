import django_filters
from .models import Product
from django.contrib.auth import get_user_model

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Search in posts (by product name):')
    product_owner = django_filters.ModelChoiceFilter(
    	queryset = get_user_model().objects.filter(role='admin'),
    	field_name = 'product_owner',
    	label = 'Product owner',
    	empty_label='-- All product owner --'
    )

    ordering = django_filters.OrderingFilter(
    	fields = (('date', 'date'), ),
    	field_labels = {'date':'Published time'},
    	label = 'Sort By'
    )

    class Meta:
    	model = Product
    	fields = ('name', 'product_owner', 'ordering')
