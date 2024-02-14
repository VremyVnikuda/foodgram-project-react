# Generated by Django 3.2.3 on 2024-02-07 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_recipe_unique recipe name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique recipe name',
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingridients', to='recipes.ingredient'),
        ),
    ]