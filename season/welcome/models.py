# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.utils.html import format_html
from django.urls import reverse
from transliterate import translit, exceptions
from notifications.signals import notify
from django.contrib.auth.models import User
from PIL import Image
import os
import glob


# сохраняет картинки с правильными именами
def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


#******************************************************************************

class CarouselElement(models.Model):
    name = models.CharField(max_length=30, verbose_name=('Заголовок элемента'))
    description = models.TextField(max_length=250, verbose_name=('Текст верхний'))
    subscription = models.TextField(max_length=300, blank=True, verbose_name=('Текст нижний'))
    available = models.BooleanField(default=True, verbose_name=('Элемент видим на сайте'))
    button = models.CharField(max_length=30, blank=True, verbose_name=('Текст в кнопке'))
    link = models.CharField(max_length=300, blank=True, verbose_name=('Ссылка'))
    image = models.ImageField(upload_to=image_folder, blank=True, verbose_name=('Изображение'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))	

    class Meta:
        verbose_name = 'Элемент карусели'
        verbose_name_plural = 'Элементы карусели'

    def __str__(self):
        return self.name      

def pre_save_carousel_element_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.name), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.name))
        instance.slug = slug

pre_save.connect(pre_save_carousel_element_slug, sender=CarouselElement)

#******************************************************************************

class Part(models.Model):
    name = models.CharField(max_length=100, verbose_name=('Название темы'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))	
    image = models.ImageField(upload_to=image_folder, default='no_foto.jpg', verbose_name=('Изображение темы'))

    class Meta:
        verbose_name = 'Тема товаров'
        verbose_name_plural = 'Темы товаров'

    def is_available(self):
        categories_of_part = Category.objects.filter(part=self)
        for category in categories_of_part:
            if category.is_available():
                return True
        return False

    def get_absolute_url(self):
    	return reverse('part_detail', kwargs={'part_slug': self.slug})   
    def __str__(self):
    	return self.name

def pre_save_part_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.name), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.name))
        instance.slug = slug

pre_save.connect(pre_save_part_slug, sender=Part)

#******************************************************************************

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=('Название категории'))
    part = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name=('Тема'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))	
    image = models.ImageField(upload_to=image_folder, default='no_foto.jpg', verbose_name=('Изображение категории'))

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def is_available(self):
        subcategories_of_category = SubCategory.objects.filter(category=self)
        for subcategory in subcategories_of_category:
            if subcategory.is_available():
                return True
        return False   
        
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})        
    def __str__(self):
        return self.name

def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.name), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.name))
        instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)

#******************************************************************************
class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=('Название подкатегории'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=('Категория'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))	
    image = models.ImageField(upload_to=image_folder, default='no_foto.jpg', verbose_name=('Изображение подкатегории'))

    class Meta:
        verbose_name = 'Подкатегория товаров'
        verbose_name_plural = 'Подкатегории товаров'

    def is_available(self):
        products_of_subcategory = Product.objects.filter(subcategory=self, available=True)
        return True if products_of_subcategory else False   

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'subcategory_slug': self.slug})        
    def __str__(self):
        return self.name

def pre_save_subcategory_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.name), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.name))
        instance.slug = slug

pre_save.connect(pre_save_subcategory_slug, sender=SubCategory)

#******************************************************************************
class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=('Бренд'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))
    def __str__(self):
    	return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

def pre_save_brand_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.name), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.name))
        instance.slug = slug

pre_save.connect(pre_save_brand_slug, sender=Brand)

#******************************************************************************

class Product(models.Model):    
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=('Подкатегория товара'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=('Бренд товара'))
    title = models.CharField(max_length=120, verbose_name=('Наименование товара'))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=('Стоимость товара'))
    available = models.BooleanField(default=True, verbose_name=('Товар доступен к заказу'))
    image = models.ImageField(upload_to=image_folder, default='no_foto.jpg', verbose_name=('Изображение товара'))
    description = models.TextField(blank=True, verbose_name=('Описание товара'))
    slug = models.SlugField(blank=True, verbose_name=('Слаг (заполняется автоматически)'))

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
    	return self.title  
    # для ссылок на обьекты
    def get_absolute_url(self):
    	return reverse('product_detail', kwargs={'product_slug': self.slug})    

def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            slug = slugify(translit(str(instance.title), reversed=True))
        except exceptions.LanguageDetectionError:
            slug = slugify(str(instance.title))
        instance.slug = slug + '-' + str(instance.id)

pre_save.connect(pre_save_product_slug, sender=Product)
		

#******************************************************************************
# элемент корзины
class CartItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=('Выбранный товар'))
    qty = models.PositiveIntegerField(default=1, verbose_name=('Количество выбранного товара'))
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name=('Итоговая стоимость товара'))

    class Meta:
        verbose_name = 'Товар из корзины'
        verbose_name_plural = 'Товары из корзины'

    def __str__(self):
        return "{0} x {1}".format(self.qty, self.product.title)


#******************************************************************************
# корзина
class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True, verbose_name=('Выбранные товары'))
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name=('Стоимость корзины'))

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return 'Корзина №' + str(self.id)

    def cart_price(self):
        return format_html('<strong>' + str(self.cart_total) + ' &#8381;' + '</strong>')

    def cart(self):
        return 'Корзина №' + str(self.id)

    def cart_items(self):
        cart = self
        prices = [str(item.product.price) + ' &#8381;' for item in cart.items.all()]
        qtys = [str(item.qty) for item in cart.items.all()]
        t_prices = [str(item.item_total) + ' &#8381;' for item in cart.items.all()]
        itms = [str(item.product.title) for item in cart.items.all()]
        return_table = '<table>'
        for n in range(len(itms)):
            s = '<tr>' +\
                '<th style="width: 85px; padding: 0; text-align: right;">' + str(prices[n]) + '</th>' +\
                '<th style="width: 50px; padding: 0; text-align: right;">' + str(qtys[n]) + 'шт.' + '</th>' +\
                '<th style="width: 90px; padding: 0; text-align: right;">' + str(t_prices[n]) + '</th>' +\
                '<th style="width: 20px; padding: 0"></th>' +\
                '<th style="padding: 0">' + str(itms[n]) + '</th>' +\
                '</tr>'
            return_table += s
        return_table += '</table>'
        return format_html(return_table)     

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

#******************************************************************************
# заказ
ORDER_STATUS_CHOICES = (
	('Принят в обработку', 'Принят в обработку'),
	('Ожидает оплаты', 'Ожидает оплаты'),
	('Оплачен, выполняется', 'Оплачен, выполняется'),
	('Ожидает получения', 'Ожидает получения'),
	('Выполнен', 'Выполнен')
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=('Логин пользователя'))
    items = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=('Номер корзины'))
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name=('Стоимость заказа'))
    first_name = models.CharField(max_length=200, verbose_name=('Имя пользователя'))
    phone = models.CharField(max_length=20, verbose_name=('Контактный телефон'))
    comments = models.TextField(blank=True, verbose_name=('Комментарии к заказу'))
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0], verbose_name=('Статус заказа'))
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def order(self):
        return 'Заказ №' + str(self.id)

    def order_price(self):
        return format_html('<strong>' + str(self.items.cart_total) + ' &#8381;' + '</strong>')

    def cart_items(self):
        cart = self.items
        prices = [str(item.product.price) + ' &#8381;' for item in cart.items.all()]
        qtys = [str(item.qty) for item in cart.items.all()]
        t_prices = [str(item.item_total) + ' &#8381;' for item in cart.items.all()]
        itms = [str(item.product.title) for item in cart.items.all()]
        return_table = '<table>'
        for n in range(len(itms)):
            s = '<tr>' +\
                '<th style="width: 85px; padding: 0; text-align: right;">' + str(prices[n]) + '</th>' +\
                '<th style="width: 50px; padding: 0; text-align: right;">' + str(qtys[n]) + 'шт.' + '</th>' +\
                '<th style="width: 90px; padding: 0; text-align: right;">' + str(t_prices[n]) + '</th>' +\
                '<th style="width: 20px; padding: 0"></th>' +\
                '<th style="padding: 0">' + str(itms[n]) + '</th>' +\
                '</tr>'
            return_table += s
        return_table += '</table>'
        return format_html(return_table)     

    def __str__(self):
        return "Заказ №{0}".format(str(self.id))