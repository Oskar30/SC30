# Generated by Django 4.1.7 on 2023-11-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0010_spare'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='author',
            field=models.CharField(blank=True, max_length=100, verbose_name='Автор'),
        ),
    ]