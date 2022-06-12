from django.shortcuts import render
from django.http import JsonResponse
from django.template.response import TemplateResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder, clearCart

from .models import Customer, Category


def home(request):
    data = cartData(request)

    cartItems = data['cartItems']

    context = {'cartItems': cartItems}

    return render(request, 'store/home.html', context)

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']

    user = request.user
    if user.is_authenticated and user.customer.predicted_age:
        products = Category.objects.get(
            interval=user.customer.age,
            gender=user.customer.gender + 1).product_set.all()
    else:
        products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(
	    customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(
	    order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
    response = TemplateResponse(request, 'store/payment_complete.html', {'cartItems': 0})
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        order.orderitem_set.clear()
    else:
        response.delete_cookie('cart')

    return response
