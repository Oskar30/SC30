# Generated by Django 4.1.7 on 2023-10-22 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0009_expenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, max_length=3000, verbose_name='Описание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
                'ordering': ['-time_create'],
            },
        ),
    ]