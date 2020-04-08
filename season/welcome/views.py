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

    categories = Category.objects.all()
    parts = Part.objects.all()
    carousel_elements = CarouselElement.objects.all()
    
    context = {
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
    context = {
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

	categories = Category.objects.all()
	parts = Part.objects.all()
	
	context = {
		'categories': categories, 
		'parts': parts, 
		"cart": cart, 
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
	categories_of_part = Category.objects.filter(part=part)
	
	for category in categories_of_part:
		subcategories_of_category = SubCategory.objects.filter(category=category)
		for subcategory in subcategories_of_category:
			if Product.objects.filter(subcategory=subcategory, available=True):
				break
		
	context = {
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

	# для динамического отображения ПОДКАТЕГОРИЙ (get_available==True) на странице category.html
	subcategories_of_category = SubCategory.objects.filter(category=category)
	for subcategory in subcategories_of_category:
		if subcategory.get_available(subcategory=subcategory):
			continue
		# удалить неподходящий

	# для динамического отображения продуктов КАТЕГОРИИ (available==True) на странице category.html
	products_of_category = []	
	products = Product.objects.all()
	for subcategory in subcategories_of_category:
		products_of_category += Product.objects.filter(subcategory=subcategory, available=True)

	context = {
        'parts': parts, 
		'categories': categories, 
		'category': category, 
		'subcategories_of_category': subcategories_of_category,
		'products_of_category': products_of_category,
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
    products_of_subcategory = Product.objects.filter(subcategory=subcategory)
    context = {
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

    context = {
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

	context = {
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
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	parts = Part.objects.all()
	context = {
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
	context = {
		'cart': cart,
        'categories': categories, 
        'parts': parts, 
	}
	if form.is_valid():
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		address = form.cleaned_data['address']
		comments = form.cleaned_data['comments']
		new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.cart_total,
			first_name=name,
			last_name=last_name,
			phone=phone,
			address=address,
			buying_type=buying_type,
			comments=comments, 
		)
		del request.session['cart_id']
		del request.session['total']
		return render(request, 'thank_you.html', context)
	return render(request, 'order.html', context)

def thank_you_view(request):
	categories = Category.objects.all()
	parts = Part.objects.all()
	context = {
        'categories': categories, 
        'parts': parts, 
	}
	return render(request, 'thank_you.html', context)

def account_view(request):
	order = Order.objects.filter(user=request.user).order_by('-id')
	username = request.user.username
	categories = Category.objects.all()
	parts = Part.objects.all()
	context = {
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
	context = {
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

	context = {
		'form': form,
        'categories': categories, 
        'parts': parts, 
	}
	return render(request, 'login.html', context)