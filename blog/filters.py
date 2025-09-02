import django_filters
from .models import Blog
from django.contrib.auth import get_user_model

class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search in posts (by title):')
    author = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.filter(role='admin'),
        field_name='author',
        label='Post author',
        empty_label='-- All authors --'
    )
    ordering = django_filters.OrderingFilter(
        fields=(('date', 'date'), ),
        field_labels={'date': 'Published time'},
        label='Sort By'
    )

    class Meta:
        model = Blog
        fields = ('title', 'author', 'ordering')
