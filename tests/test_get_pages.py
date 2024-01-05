import pytest
from django.urls import reverse


def test_view_home(client):
   url = reverse('home')
   response = client.get(url)
   assert response.status_code == 200

def test_view_repair(client):
   url = reverse('repair')
   response = client.get(url)
   assert response.status_code == 200


def test_view_orders_user(client):
   url = reverse('orders')
   response = client.get(url)
   assert response.status_code == 302

def test_view_orders_admin(admin_client):
   url = reverse('orders')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_orders_done_user(client):
   url = reverse('orders_done')
   response = client.get(url)
   assert response.status_code == 302

def test_view_orders_done_admin(admin_client):
   url = reverse('orders_done')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_add_order_user(client):
   url = reverse('add_order')
   response = client.get(url)
   assert response.status_code == 302

def test_view_add_order_admin(admin_client):
   url = reverse('add_order')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_expenses_user(client):
   url = reverse('expenses')
   response = client.get(url)
   assert response.status_code == 302

def test_view_expenses_admin(admin_client):
   url = reverse('expenses')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_add_expenses_user(client):
   url = reverse('add_expenses')
   response = client.get(url)
   assert response.status_code == 302

def test_view_add_expenses_admin(admin_client):
   url = reverse('add_expenses')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_stock_user(client):
   url = reverse('stock')
   response = client.get(url)
   assert response.status_code == 302

def test_view_stock_admin(admin_client):
   url = reverse('stock')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_add_spare_user(client):
   url = reverse('add_spare')
   response = client.get(url)
   assert response.status_code == 302

def test_view_add_spare_admin(admin_client):
   url = reverse('add_spare')
   response = admin_client.get(url)
   assert response.status_code == 200


def test_view_cashbox_user(client):
   url = reverse('cashbox')
   response = client.get(url)
   assert response.status_code == 302

def test_view_cashbox_admin(admin_client):
   url = reverse('cashbox')
   response = admin_client.get(url)
   assert response.status_code == 200