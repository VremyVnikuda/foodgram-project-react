from colorfield.fields import ColorField
from django.core import validators
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель Ингредиенты."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient measurement_unit'
            )]
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель Тэг."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        unique=True,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text="Выберите ингредиенты."
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        verbose_name='Тэги',
        help_text="Выберите один или несколько тэгов."
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления блюда, мин.',
        validators=[
            validators.MinValueValidator(
                1,
                message=(
                    'Время приготовления должно быть не меньше',
                    f'{1}!'
                )
            ),
            validators.MaxValueValidator(
                4320,
                message=(
                    'Время приготовления не должно быть больше',
                    f'{4320}!'
                )
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации рецепта'
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}, {self.author}'


class IngredientRecipe(models.Model):
    """Промежуточная модель Ингридиент - Рецепт."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1,
                message=(
                    'Количество ингридиента не может быть меньше',
                    f'{1}!'
                )
            ),
            validators.MaxValueValidator(
                32000,
                message=(
                    'Количество ингридиента не может быть больше',
                    f'{32000}!'
                )
            ),
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient'
            )]
        ordering = ('recipe', )
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'Рецепт {self.recipe} содержит {self.ingredient}.'


class TagRecipe(models.Model):
    """Промежуточная модель Тэг - Рецепт."""

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )

    class Meta:
        ordering = ('tag', )
        verbose_name = 'тег рецепта'
        verbose_name_plural = 'теги рецепта'

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class CustomModel(models.Model):
    """Кастомная модель для наследования моделей Избранное и Список покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Выбранный рецепт'
    )

    class Meta:
        abstract = True
        ordering = ('user', )

    def __str__(self):
        return (f'Пользователь {self.user} '
                f'добавил рецепт {self.recipe} в {self._meta.verbose_name}.')


class Favorite(CustomModel):
    """Модель Избранное."""

    class Meta(CustomModel.Meta):
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )


class ShoppingCart(CustomModel):
    """Модель Список покупок."""

    class Meta(CustomModel.Meta):
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_cart'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_shopping_cart'
            ),
        )
