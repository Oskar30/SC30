from django.urls import path
from workshop import views

urlpatterns = [
    path('', views.Repair.as_view(), name='repair'),
    path('orders/', views.Orders.as_view(), name='orders'),
    path('orders/addorder/', views.AddOrder.as_view(), name='add_order'),
    path('orders/<int:pk>', views.UpdateOrder.as_view(), name='update_order'),
    path('cashbox/', views.Cashbox.as_view(), name='cashbox'),

]
