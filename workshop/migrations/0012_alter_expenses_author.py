# Generated by Django 4.1.7 on 2023-11-01 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0011_expenses_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='author',
            field=models.CharField(max_length=60, verbose_name='Автор'),
        ),
    ]