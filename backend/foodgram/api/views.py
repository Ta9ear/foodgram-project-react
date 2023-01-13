from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import (decorators, generics, permissions, status,
                            views, viewsets)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import FavoriteShoppingCartView
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                             IngredientSerializer, RecipeSerializer,
                             ShoppingCartSerializer,
                             SubscriptionRepresentationSerializer,
                             SubscriptionSerializer, TagSerializer)
from users.models import Subscription

CustomUser = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Recipe model viewset: list/create/retrieve/partial_update/destroy
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ingredient model viewset, read only: list, retrieve
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tag model viewset, read only: list, retrieve
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FavoriteView(FavoriteShoppingCartView):
    """
    Favorite model api view: create, destroy
    """
    model = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


class SubscriptionView(views.APIView):
    """
    Subscription model api view: create/destroy
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        if not Subscription.objects.filter(
                user=request.user, author__id=id
        ).exists() and id != request.user.id:
            serializer = SubscriptionSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        author = get_object_or_404(CustomUser, id=id)
        if Subscription.objects.filter(
                user=request.user,
                author=author
        ).exists():
            subsription_obj = get_object_or_404(
                Subscription, user=request.user, author=author
            )
            subsription_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionRepresentationView(generics.ListAPIView):
    """
    Subscription list representation listapi generic view
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(author__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionRepresentationSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class ShoppingCartView(FavoriteShoppingCartView):
    """
    ShoppingCart model api view: create/destroy
    """
    model = ShoppingCart
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]


@decorators.api_view(['GET'])
def download_shopping_cart(request):
    """
    Shopping cart downloading api view: retrieve
    """
    ingredient_list = "Cписок покупок:"
    ingredients = RecipeIngredient.objects.filter(
        recipe__shoppingcart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(amount_sum=Sum('amount'))
    for num, i in enumerate(ingredients):
        ingredient_list += (
            f"\n{i['ingredient__name']} - "
            f"{i['amount_sum']} {i['ingredient__measurement_unit']}"
        )
        if num < ingredients.count() - 1:
            ingredient_list += ', '
    file = 'shopping_list'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
