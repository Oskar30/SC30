from django.urls import path
from workshop import views

urlpatterns = [
    path('', views.Repair.as_view(), name='repair'),
    
    path('orders/', views.Orders.as_view(), name='orders'),
    path('orders/done/', views.OrdersDone.as_view(), name='orders_done'),
    path('orders/addorder/', views.AddOrder.as_view(), name='add_order'),
    path('orders/<int:pk>/', views.UpdateOrder.as_view(), name='update_order'),
    path('orders/<int:pk>/delete/', views.DeleteOrder.as_view(), name='delete_order'),
    
    path('expenses/', views.Expenses.as_view(), name='expenses'),
    path('expenses/addexpenses/', views.AddExpenses.as_view(), name='add_expenses'),
    path('expenses/<int:pk>/', views.UpdateExpenses.as_view(), name='update_expenses'),
    path('expenses/<int:pk>/delete/', views.DeleteExpenses.as_view(), name='delete_expenses'),

    path('stock/', views.Stock.as_view(), name='stock'),
    path('stock/addspare/', views.AddSpare.as_view(), name='add_spare'),
    path('stock/<int:pk>/', views.UpdateSpare.as_view(), name='update_spare'),
    path('stock/<int:pk>/delete/', views.DeleteSpare.as_view(), name='delete_spare'),

    path('cashbox/', views.Cashbox.as_view(), name='cashbox'),

]
