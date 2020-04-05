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
	list_display = (Cart.name, Cart.cart_items, Cart.item_price, Cart.quantity, Cart.total_item_price, Cart.cart_price)

admin.site.register(Part)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CarouselElement)