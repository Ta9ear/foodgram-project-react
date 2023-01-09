from django.contrib.admin import ModelAdmin, TabularInline, register, site
from recipes.models import (Recipe, Ingredient, Tag, RecipeIngredient,
                            ShoppingCart, Favorite)


class IngredientsInline(TabularInline):
    model = RecipeIngredient
    extra = 3


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    filter_horizontal = ('tags', )
    inlines = (IngredientsInline, )


models_list = [Ingredient, Tag, ShoppingCart, Favorite]
for model in models_list:
    site.register(model)
