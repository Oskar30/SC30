from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from workshop import models, forms
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
# import datetime
from datetime import datetime, date

import logging

logger = logging.getLogger('main')


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


class Orders(LoginRequiredMixin, ListView):
    model = models.Order
    # paginate_by = 10
    template_name = "workshop/orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddOrder(LoginRequiredMixin, CreateView):
    form_class = forms.AddOrderForm
    template_name = 'workshop/order_add.html'
    success_url = reverse_lazy('orders')
    # login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateOrder(LoginRequiredMixin, UpdateView):
    model = models.Order
    fields = ["person", "contact", "title",
              "description", "status", "price", "expenses"]
    # success_url = reverse_lazy('orders')
    template_name = "workshop/order_update.html"

    def form_valid(self, form):
        form.save()
        logger.info(f"{form.initial} -> {form.cleaned_data}")
        return redirect('orders')
    

#class DeleteOrder(DeleteView):
#    model = models.Order
#    success_url = reverse_lazy('orders')


class Expenses(LoginRequiredMixin, ListView):
    model = models.Expenses
    template_name = "workshop/expenses.html"
    context_object_name = "expenses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddExpenses(LoginRequiredMixin, CreateView):
    form_class = forms.AddExpensesForm
    template_name = 'workshop/expenses_add.html'
    success_url = reverse_lazy('expenses')
    # login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class UpdateExpenses(LoginRequiredMixin, UpdateView):
    model = models.Expenses
    fields = ["expenses", "sum"]
    success_url = reverse_lazy('expenses')
    template_name = "workshop/expenses_update.html"

#    def form_valid(self, form):
#        form.save()
#        logger.info(f"{form.initial} -> {form.cleaned_data}")
#        return redirect('orders')

class Cashbox(ListView):
    model = models.Order
    # paginate_by = 10
    template_name = "workshop/cashbox.html"
    
    def expenses_total(self):
        expenses = models.Expenses.objects.all()
        total = 0
        
        for expense in expenses:
            total += expense.sum

        return total
    
    def expenses_today(self):
        expenses_today = models.Expenses.objects.filter(
            time_create__gte=date.today())  # __gt __lt __gte __lte
        expenses_today_sum = 0

        for expense in expenses_today:
            expenses_today_sum += expense.sum

        return {'expenses_today':expenses_today, 'expenses_today_sum':expenses_today_sum}

    def cash_total(self):
        orders = self.model.objects.filter(status='Выполнен')
        total = 0 - self.expenses_total()

        for order in orders:
            total += order.price - order.expenses

        return total

    def cash_today(self):
        orders_today = self.model.objects.filter(
            time_update__gte=date.today()) & self.model.objects.filter(status='Выполнен')  # __gt __lt __gte __lte
        
        expenses_today = self.expenses_today()
        expenses_today_sum = expenses_today['expenses_today_sum']
        
        cash_today = 0 - expenses_today_sum
        cash_today_not_expenses = 0

        for order in orders_today:
            cash_today += order.price - order.expenses
            cash_today_not_expenses += order.price - order.expenses

        return {'orders_today': orders_today, 'cash_today': cash_today, 'cash_today_not_expenses':cash_today_not_expenses}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cash_today'] = self.cash_today()
        context['cash_total'] = self.cash_total()
        context['expenses_total'] = self.expenses_total()
        context['expenses_today'] = self.expenses_today()

        return context