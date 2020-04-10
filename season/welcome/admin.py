# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from welcome.models import Category, SubCategory, Brand, Product, CartItem, Cart, Order, Part, CarouselElement

# методы для заказов (Orders) ***************************************************************
def make_accepted(modeladmin, request, queryset):
    queryset.update(status='Принят в обработку')
make_accepted.short_description = " Пометить выбранные как 'Принят в обработку'"

def make_wait_payed(modeladmin, request, queryset):
    queryset.update(status='Ожидает оплаты')
make_wait_payed.short_description = " Пометить выбранные как 'Ожидает оплаты'"

def make_payed_process(modeladmin, request, queryset):
    queryset.update(status='Оплачен, выполняется')
make_payed_process.short_description = " Пометить выбранные как 'Оплачен, выполняется'"

def make_wait_get(modeladmin, request, queryset):
    queryset.update(status='Ожидает получения')
make_wait_get.short_description = " Пометить выбранные как 'Ожидает получения'"

def make_complete(modeladmin, request, queryset):
    queryset.update(status='Выполнен')
make_complete.short_description = " Пометить выбранные как 'Выполнен'"
# *******************************************************************************************

# методы для товаров (Products) ***************************************************************
def make_available(modeladmin, request, queryset):
    queryset.update(available=True)
make_accepted.short_description = " Пометить выбранные как 'Доступен'"

def make_not_available(modeladmin, request, queryset):
    queryset.update(available=False)
make_accepted.short_description = " Пометить выбранные как 'Не доступен'"
# *******************************************************************************************



class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_accepted, make_wait_payed, make_payed_process, make_wait_get, make_complete]
    list_display = ('order', "status", Order.order_price, Order.cart_items)

class CartAdmin(admin.ModelAdmin):
    list_display = (Cart.cart, Cart.cart_price, Cart.cart_items)    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'subcategory', 'available')   
    list_filter = ['subcategory', 'available', 'brand'] 
    actions = [make_available, make_not_available]

admin.site.register(Part)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CarouselElement)