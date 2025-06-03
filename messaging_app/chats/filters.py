import django_filters
from .models import Message
from django.contrib.auth.models import User

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    user = django_filters.ModelChoiceFilter(field_name='sender', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
