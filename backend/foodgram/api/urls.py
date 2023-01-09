from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (RecipeViewSet, IngredientViewSet, TagViewSet,
                       SubscriptionRepresentationView, FavoriteView,
                       SubscriptionView, ShoppingCartView,
                       download_shopping_cart)

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscriptionView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        SubscriptionRepresentationView.as_view(),
        name='subscription'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
