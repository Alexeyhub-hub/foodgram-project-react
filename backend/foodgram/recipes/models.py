from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class CreatedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Tag(CreatedModel):
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не соответствует формату HEX!'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['slug', ]
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'


class Ingredient(CreatedModel):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Ингридиент',
        verbose_name_plural = 'Ингридиенты'


class Recipe(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    text = models.TextField()
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(CreatedModel):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        related_name='tags',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='tag_recipes',
    )

    class Meta:
        ordering = ['tag', ]
        verbose_name = 'Теги рецепта',
        verbose_name_plural = 'Теги рецептов'


class IngredientInRecipe(CreatedModel):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredients_recipes',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients_recipes',
    )
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Ингридиенты рецепта',
        verbose_name_plural = 'Ингридиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='IngredientInRecipe'
            )
        ]

    def __str__(self):
        return (f'Количество ингредиента {self.ingredient} '
                f'для приготовления блюда {self.recipe}')


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
