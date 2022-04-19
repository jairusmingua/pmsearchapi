from django_filters import rest_framework as filters


class SongFilter(filters.FilterSet):
    artist = filters.CharFilter()
    title = filters.CharFilter()

