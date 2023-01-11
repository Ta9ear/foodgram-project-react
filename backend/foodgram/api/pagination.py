from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Custom Pagination for RecipeViewSet, FavoriteView,
    SubscriptionRepresentationView
    """
    page_size = 6
    page_size_query_param = 'limit'
