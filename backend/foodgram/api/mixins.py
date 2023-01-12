from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response

from recipes.models import Recipe


class FavoriteShoppingCartView(views.APIView):
    """
    Favorite ShoppingCart model api view: create/destroy
    """
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        if not self.model.objects.filter(
                user=request.user,
                recipe__id=id
        ).exists():
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if self.model.objects.filter(
                user=request.user, recipe=recipe).exists():
            self.model.objects.filter(
                user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
