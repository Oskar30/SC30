from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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

    author = models.ForeignKey(User, related_name="Orders", verbose_name="Автор", on_delete=models.PROTECT)

    title = models.CharField(max_length=100, verbose_name="Вид\модель техники")
    description = models.TextField(max_length=3000, blank=True, verbose_name="Описание")

    status = models.CharField(max_length=15, default="Диагностика", verbose_name="Статус", choices = CHOICES)
    price = models.IntegerField(default=0, null=True, verbose_name="Цена")
    expenses = models.PositiveIntegerField(default=0, null=True, verbose_name="Затраты")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self) -> str:
        return self.title
    
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

    author = models.ForeignKey(User, related_name="Expenses", verbose_name="Автор", on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.expenses
    
    def get_absolute_url(self):
        return reverse('update_expenses', kwargs={'pk':self.pk})
    
    class Meta:
        verbose_name = "Расходы"
        verbose_name_plural = "Расходы"
        ordering = ['-time_create',]


class Spare(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(max_length=3000, blank=True, verbose_name="Описание")

    author = models.ForeignKey(User, related_name="Spares", verbose_name="Автор", on_delete=models.PROTECT)

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('update_spare', kwargs={'pk':self.pk})
    
    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
        ordering = ['-time_create',]