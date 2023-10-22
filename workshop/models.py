from django.db import models
from django.urls import reverse


CHOICES = (
        ('Диагностика', 'Диагностика'),
        ('В работе', 'В работе'),
        ('Готов', 'Готов'),
        ('Выполнен', 'Выполнен'),
        ('Отменен', 'Отменен'),
    )


class Order(models.Model):
    person = models.CharField(max_length=100, blank=False, verbose_name="Клиент")
    contact = models.PositiveBigIntegerField(blank=False, default=0, verbose_name="Контакты")

    title = models.CharField(max_length=100, verbose_name="Вид\модель техники")
    description = models.TextField(max_length=3000, blank=True, verbose_name="Описание")

    status = models.CharField(max_length=60, default="Диагностика", verbose_name="Статус", choices = CHOICES)
    price = models.IntegerField(default=0, null=True, verbose_name="Цена")
    expenses = models.PositiveIntegerField(default=0, null=True, verbose_name="Затраты")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self) -> str:
        return f'Заказ №{self.id}: {self.title}'
    
    def get_absolute_url(self):
        return reverse('update_order', kwargs={'pk':self.pk})
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-time_create',]


class Expenses(models.Model):
    expenses = models.CharField(max_length=300, blank=False, verbose_name="Затраты")
    sum = models.PositiveIntegerField(default=0, null=True, verbose_name="Сумма")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def get_absolute_url(self):
        return reverse('update_expenses', kwargs={'pk':self.pk})
