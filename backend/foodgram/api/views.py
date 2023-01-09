from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets, permissions, views, filters,
                            status, generics, decorators)
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.pagination import CustomPagination
from recipes.models import (Recipe, Ingredient, Tag, Favorite,
                            ShoppingCart, RecipeIngredient)
from users.models import CustomUser, Subscription
from api.serializers import (RecipeSerializer, CreateRecipeSerializer,
                             IngredientSerializer, TagSerializer,
                             FavoriteSerializer, SubscriptionSerializer,
                             SubscriptionRepresentationSerializer,
                             ShoppingCartSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
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
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FavoriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not Favorite.objects.filter(
                user=request.user,
                recipe__id=id
        ).exists():
            serializer = FavoriteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        if not Subscription.objects.filter(
                user=request.user, author__id=id
        ).exists():
            serializer = SubscriptionSerializer(
                data=data,
                context={'request': request}
            )
            if serializer.is_valid():
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


class ShoppingCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        recipe = get_object_or_404(Recipe, id=id)
        if not ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
        ).exists():
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
        ).exists():
            shopping_cart_obj = get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe
            )
            shopping_cart_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET'])
def download_shopping_cart(request):
    ingredient_list = "Cписок покупок:"
    ingredients = RecipeIngredient.objects.filter(
        recipe__shoppingcart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for num, i in enumerate(ingredients):
        ingredient_list += (
            f"\n{i['ingredient__name']} - "
            f"{i['amount']} {i['ingredient__measurement_unit']}"
        )
        if num < ingredients.count() - 1:
            ingredient_list += ', '
    file = 'shopping_list'
    response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
    return response
