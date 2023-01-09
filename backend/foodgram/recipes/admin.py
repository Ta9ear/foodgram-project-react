from django.contrib.admin import ModelAdmin, TabularInline, register, site
from recipes.models import (Recipe, Ingredient, Tag, RecipeIngredient,
                            ShoppingCart, Favorite)


class IngredientsInline(TabularInline):
    model = RecipeIngredient
    extra = 3


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags', )
    inlines = (IngredientsInline, )


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_filter = ('name',)


models_list = [Tag, ShoppingCart, Favorite]
for model in models_list:
    site.register(model)
