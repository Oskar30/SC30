from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from workshop import models, forms
from django.views.generic import ListView, DetailView, CreateView
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
    template_name = 'workshop/addorder.html'
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
    template_name = "workshop/update_order.html"

    def form_valid(self, form):
        form.save()
        logger.info(f"{form.initial} -> {form.cleaned_data}")
        return redirect('orders')


class Cashbox(ListView):
    model = models.Order
    # paginate_by = 10
    template_name = "workshop/cashbox.html"

    def cash_total(self):
        orders = self.model.objects.filter(status='Выполнен')
        total = 0

        for order in orders:
            total += order.price - order.expenses

        return total

    def cash_today(self):
        orders_today = self.model.objects.filter(
            time_create__gte=date.today()) & self.model.objects.filter(status='Выполнен')  # __gt __lt __gte __lte
        cash_today = 0

        for order in orders_today:
            cash_today += order.price - order.expenses

        return {'orders_today': orders_today, 'cash_today': cash_today}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cash_today'] = self.cash_today

        context['cash_total'] = self.cash_total

        return context

#test

