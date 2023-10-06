import django_filters
from django import forms
from core.models import News, Tag


class NewsFilter(django_filters.FilterSet):

    date_range = django_filters.DateRangeFilter(field_name='date')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = News
        fields = ('tags', 'category', 'author')
