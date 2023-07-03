from django_filters import FilterSet, NumberFilter, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
