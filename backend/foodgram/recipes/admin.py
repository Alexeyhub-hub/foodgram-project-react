from django.contrib import admin

from .models import (Favourite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(TagRecipe)
admin.site.register(IngredientInRecipe)
admin.site.register(Favourite)
admin.site.register(ShoppingCart)
