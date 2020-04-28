# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from welcome.forms import OrderForm, RegistrationForm, LoginForm
from welcome.models import Category, SubCategory, Product, CartItem, Cart, Order, Part, CarouselElement
from django.views.generic import View
from django.contrib.auth.models import User
from random import shuffle

# Create your views here.
def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)	
    user_groups = list(request.user.groups.values_list('name', flat=True))
    categories = Category.objects.all()
    parts_temp = Part.objects.all()
    parts = []
    for part in parts_temp:
    	if part.is_available():
    		parts += parts_temp.filter(name=part.name)	
    carousel_elements = CarouselElement.objects.filter(available=True)

    context = {
        'user_groups': user_groups,
        'categories': categories, 
        'parts': parts, 
        "cart": cart, 
    	'carousel_elements': carousel_elements,
    }
    return render(request, 'base.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    parts = Part.objects.all()
    user_groups = list(request.user.groups.values_list('name', flat=True))
    context = {
        'user_groups': user_groups,
        'product': product, 
        'categories': categories, 
        'parts': parts, 
        'cart': cart, 
    }
    return render(request, 'product.html', context)

def catalog_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)	
	categories_temp = Category.objects.all()
	categories = []
	for category in categories_temp:
		if category.is_available():
			categories += categories_temp.filter(name=category.name)	
	parts_temp = Part.objects.all()
	parts = []
	for part in parts_temp:
		if part.is_available():
			parts += parts_temp.filter(name=part.name)	

	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'categories': categories, 
		'parts': parts, 
		'cart': cart, 
	}
	return render(request, 'catalog.html', context)

def part_view(request, part_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	parts = Part.objects.all()
	categories = Category.objects.all()
	part = Part.objects.get(slug=part_slug)	
	categories_of_part_temp = Category.objects.filter(part=part)	
	categories_of_part = []
	for category in categories_of_part_temp:
		if category.is_available():
			categories_of_part += categories_of_part_temp.filter(name=category.name)

	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'parts': parts, 
		'categories': categories, 
	    'part': part, 
		'categories_of_part': categories_of_part,
		'cart': cart
	}
	return render(request, 'part.html', context)

def category_view(request, category_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	parts = Part.objects.all()
	categories = Category.objects.all()
	category = Category.objects.get(slug=category_slug)	
	# для динамического отображения ПОДКАТЕГОРИЙ с is_available==True на странице category.html
	# TODO
	subcategories_of_category_temp = SubCategory.objects.filter(category=category)
	subcategories_of_category = []
	for subcategory in subcategories_of_category_temp:
		if subcategory.is_available():
			subcategories_of_category += subcategories_of_category_temp.filter(name=subcategory.name)
			continue    	
	# для динамического отображения ПРОДУКТОВ с признаком available==True на странице category.html
	# TODO
	products_of_category = Product.objects.none()
	for subcategory in subcategories_of_category:
		products_of_category = products_of_category | Product.objects.filter(subcategory=subcategory, available=True)	
	len_products_of_category = len(products_of_category)
	if len_products_of_category > 30:
		products_of_category = list(products_of_category)
		shuffle(products_of_category)
		products_of_category = products_of_category[:30]
	else:
		products_of_category = products_of_category.order_by('title')	
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
	    'parts': parts, 
		'categories': categories, 
		'category': category, 
		'subcategories_of_category': subcategories_of_category,
		'products_of_category': products_of_category,
		'len_products_of_category': len_products_of_category,
		'cart': cart
	}
	return render(request, 'category.html', context)

def subcategory_view(request, subcategory_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    parts = Part.objects.all()
    categories = Category.objects.all()
    subcategory = SubCategory.objects.get(slug=subcategory_slug)
    price_filter_type = request.GET.get('price_filter_type')
    products_of_subcategory = Product.objects.filter(subcategory=subcategory).order_by('title')
    user_groups = list(request.user.groups.values_list('name', flat=True))
    context = {
        'user_groups': user_groups,
        'parts': parts, 
        'categories': categories, 
        'subcategory': subcategory, 
        'products_of_subcategory': products_of_subcategory,
        'cart': cart
    }
    return render(request, 'subcategory.html', context)

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all()
    parts = Part.objects.all()

    user_groups = list(request.user.groups.values_list('name', flat=True))
    context = {
        'user_groups': user_groups,
        'cart': cart, 
        'categories': categories, 
        'parts': parts, 
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get("product_slug")
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({
		'cart_total': cart.items.count(), 
		'cart_total_price': cart.cart_total,
		})
        
def remove_from_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	product_slug = request.GET.get('product_slug')
	product = Product.objects.get(slug=product_slug)
	cart.remove_from_cart(product.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})

def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({
		'cart_total': cart.items.count(), 
        'item_total': cart_item.item_total,
		'cart_total_price': cart.cart_total,
		})

def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)	
	categories = Category.objects.all()
	parts = Part.objects.all()	
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'cart': cart,
	    'categories': categories, 
	    'parts': parts, 
	}
	return render(request, 'checkout.html', context)

def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	first_name = request.user.first_name
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	parts = Part.objects.all()
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'first_name': first_name,
		'form': form,
		'cart': cart,
	    'categories': categories, 
	    'parts': parts, 
	}
	return render(request, 'order.html', context)

def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	parts = Part.objects.all()	
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'cart': cart,
	    'categories': categories, 
	    'parts': parts, 
	}
	if form.is_valid():
		name = form.cleaned_data['name']
		phone = form.cleaned_data['phone']
		comments = form.cleaned_data['comments']
		new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.cart_total,
			first_name=name,
			phone=phone,
			comments=comments, 
		)
		del request.session['cart_id']
		del request.session['total']
		return render(request, 'thank_you.html', context)
	return render(request, 'order.html', context)

def thank_you_view(request):
	categories = Category.objects.all()
	parts = Part.objects.all()
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
	    'categories': categories, 
	    'parts': parts, 
	}
	return render(request, 'thank_you.html', context)

def account_view(request):
	order = Order.objects.filter(user=request.user).order_by('-id')
	username = request.user.username
	categories = Category.objects.all()
	parts = Part.objects.all()
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'order': order,
	    'categories': categories, 
	    'parts': parts, 
		'username': username,
	}
	return render(request, 'account.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	parts = Part.objects.all()
	if form.is_valid():
		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		new_user.username = username
		new_user.set_password(password)
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.email = email
		new_user.save()
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'form': form,
	    'categories': categories, 
	    'parts': parts, 
	}
	return render(request, 'registration.html', context)


def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))	
	categories = Category.objects.all()
	parts = Part.objects.all()	
	user_groups = list(request.user.groups.values_list('name', flat=True))
	context = {
	    'user_groups': user_groups,
		'form': form,
	    'categories': categories, 
	    'parts': parts, 
	}
	return render(request, 'login.html', context)