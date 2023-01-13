from django.contrib.admin import ModelAdmin, TabularInline, register, site

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class IngredientsInline(TabularInline):
    model = RecipeIngredient
    extra = 3


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('author', 'name', 'favorite_count')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags', )
    inlines = (IngredientsInline, )

    def favorite_count(self, obj):
        return obj.favorite_set.count()


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_filter = ('name',)


models_list = [Tag, ShoppingCart, Favorite]
for model in models_list:
    site.register(model)
