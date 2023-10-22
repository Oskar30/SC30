from django.contrib import admin
from workshop import models


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'contact', 'title', 'description', 'status', 'price', 'time_create', 'time_update']
    #list_display_links = [ 'id', 'name']
    search_fields = ['title', 'price']
    #prepopulated_fields = {"slug":("name",)}

admin.site.register(models.Order, OrderAdmin)


admin.site.register(models.Expenses)