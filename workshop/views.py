from typing import Any
from django import http
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from workshop import models, forms, serializers, permissions
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime, date
from django.http import Http404
import logging
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated



logger = logging.getLogger('main')


class CustomCreateView(CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        obj = self.model.objects.filter(id=kwargs['pk'])

        try:
            author = obj[0].author
        except IndexError:
            raise Http404

        if author != self.request.user:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['del'] = self.request.path + 'delete'
        return context


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'workshop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'workshop/login.html'
    success_url = reverse_lazy('login')


def logout_user(request):
    logout(request)
    return redirect('login')


class Index(TemplateView):
    template_name = "workshop/index.html"


class Repair(TemplateView):
    template_name = "workshop/repair.html"


class Contact(TemplateView):
    template_name = "workshop/contact.html"


class Orders(LoginRequiredMixin, TemplateView):
    template_name = "workshop/orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        orders = models.Order.objects.filter(author=user)
        context['orders'] = orders

        return context
    

class OrdersDone(LoginRequiredMixin, TemplateView):
    template_name = "workshop/ordersdone.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        orders = models.Order.objects.filter(author=user)
        context['orders'] = orders

        return context


# Заменить на PermissionRequiredMixin
# при добавлении пользователей-клиентов
class AddOrder(LoginRequiredMixin, CustomCreateView):
    form_class = forms.AddOrderForm
    template_name = 'workshop/add.html'
    success_url = reverse_lazy('orders')


class UpdateOrder(CustomLoginRequiredMixin, UpdateView):
    model = models.Order
    fields = ["person", "contact", "title",
              "description", "status", "price", "expenses"]
    template_name = "workshop/update.html"

    def form_valid(self, form):                             # улучшить логирование
        form.save()
        logger.info(f"{form.initial} -> {form.cleaned_data}")
        return redirect('orders')


class DeleteOrder(CustomLoginRequiredMixin, DeleteView):
    model = models.Order
    success_url = reverse_lazy('orders')
    template_name = "workshop/delete.html"


class Expenses(LoginRequiredMixin, TemplateView):
    template_name = "workshop/expenses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        expenses = models.Expenses.objects.filter(author=user)
        context['expenses'] = expenses

        return context


class AddExpenses(LoginRequiredMixin, CustomCreateView):
    form_class = forms.AddExpensesForm
    template_name = 'workshop/add.html'
    success_url = reverse_lazy('expenses')


class UpdateExpenses(CustomLoginRequiredMixin, UpdateView):
    model = models.Expenses
    fields = ["expenses", "sum"]
    success_url = reverse_lazy('expenses')
    template_name = "workshop/update.html"


class DeleteExpenses(CustomLoginRequiredMixin, DeleteView):
    model = models.Expenses
    success_url = reverse_lazy('expenses')
    template_name = "workshop/delete.html"


class Stock(LoginRequiredMixin, TemplateView):
    template_name = "workshop/stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        spare = models.Spare.objects.filter(author=user)
        context['spare'] = spare

        return context


class AddSpare(LoginRequiredMixin, CustomCreateView):
    form_class = forms.AddSpareForm
    template_name = 'workshop/add.html'
    success_url = reverse_lazy('stock')
    # raise_exception = True


class UpdateSpare(CustomLoginRequiredMixin, UpdateView):
    model = models.Spare
    fields = ["title", "description"]
    success_url = reverse_lazy('stock')
    template_name = "workshop/update.html"


class DeleteSpare(CustomLoginRequiredMixin, DeleteView):
    model = models.Spare
    success_url = reverse_lazy('stock')
    template_name = "workshop/delete.html"


class Cashbox(LoginRequiredMixin, TemplateView):
    template_name = "workshop/cashbox.html"
    #model = models.Order
    orders = models.Order.objects.all()
    expenses = models.Expenses.objects.all()

    def expenses_total(self):
        expenses = self.expenses.filter(author=self.request.user)
        total = 0
        for expense in expenses:
            total += expense.sum

        return total

    def expenses_today(self):
        expenses_today = self.expenses.filter(
            author=self.request.user) & self.expenses.filter(time_create__gte=date.today())

        # expenses_today = models.Expenses.objects.filter(
        #    time_create__gte=date.today())  # __gt __lt __gte __lte
        expenses_today_sum = 0

        for expense in expenses_today:
            expenses_today_sum += expense.sum

        return {'expenses_today': expenses_today, 'expenses_today_sum': expenses_today_sum}

    def cash_total(self):
        orders = self.orders.filter(
            author=self.request.user) & self.orders.filter(status='Выполнен')
        total = 0 - self.expenses_total()

        for order in orders:
            total += order.price - order.expenses

        return total

    def cash_today(self):
        orders_today = self.orders.filter(author=self.request.user) & self.orders.filter(
            time_update__gte=date.today()) & self.orders.filter(status='Выполнен')  # __gt __lt __gte __lte

        expenses_today = self.expenses_today()
        expenses_today_sum = expenses_today['expenses_today_sum']

        cash_today = 0 - expenses_today_sum
        cash_today_not_expenses = 0

        for order in orders_today:
            cash_today += order.price - order.expenses
            cash_today_not_expenses += order.price - order.expenses

        return {'orders_today': orders_today, 'cash_today': cash_today, 'cash_today_not_expenses': cash_today_not_expenses}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cash_today'] = self.cash_today()
        context['cash_total'] = self.cash_total()
        context['expenses_total'] = self.expenses_total()
        context['expenses_today'] = self.expenses_today()

        return context



class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]
    
    def get_queryset(self):
        queryset = models.Order.objects.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)