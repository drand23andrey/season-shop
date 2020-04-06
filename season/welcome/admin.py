# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from welcome.models import Category, Brand, Product, CartItem, Cart, Order, Part, CarouselElement


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]

class CartAdmin(admin.ModelAdmin):
    # list_display = (Cart.cart, Cart.cart_item, Cart.item_price, Cart.item_quantity, Cart.total_item_price, Cart.cart_price)
    list_display = (Cart.cart, Cart.cart_price, Cart.cart_items)
    

admin.site.register(Part)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CarouselElement)