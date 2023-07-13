import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Category

NEWS = 'NW'
ARTICLE = 'AR'
CATEGORY_CHOICES = [
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья'),
    ]

class PostFilter(FilterSet):
    name = django_filters.CharFilter(
            field_name='name',
            lookup_expr='icontains',
            label='Title',
        )
    #category = django_filters.ModelChoiceFilter(
        #field_name='name',
        #queryset=Category.objects.all(),
        #label='Category',
        #empty_label='Select a category',
    #)

    categoryType = django_filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        label='Category')

    #createDate = django_filters.DateFromToRangeFilter(
    #    published_after = 'incontains')

    createDate = django_filters.DateFilter(
        field_name='createDate',
        lookup_expr='lt',
        label='Date',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'}
            #attrs={'type': 'createDate'}
            ,),
    )