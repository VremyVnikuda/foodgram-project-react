# Generated by Django 3.2.3 on 2024-02-09 11:28

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20230908_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message=('Количество ингридиента не может быть меньше', '1!')), django.core.validators.MaxValueValidator(32000, message=('Количество ингридиента не может быть больше', '32000!'))]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Цветовой HEX-код'),
        ),
    ]
