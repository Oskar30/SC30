# Generated by Django 4.1.7 on 2023-11-09 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0018_alter_order_author_alter_spare_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Диагностика', 'Диагностика'), ('В работе', 'В работе'), ('Готов', 'Готов'), ('Выполнен', 'Выполнен'), ('Отменен', 'Отменен')], default='Диагностика', max_length=15, verbose_name='Статус'),
        ),
    ]
