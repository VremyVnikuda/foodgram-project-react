# Generated by Django 4.2.4 on 2024-01-30 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_subscription_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
    ]
