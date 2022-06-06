from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200)
	profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
	predicted_gender = models.BooleanField(null=True, default=False)
	predicted_age = models.BooleanField(null=True, default=False)
	# 1 - male
	# 2 - female
	gender = models.PositiveSmallIntegerField(null=True)
	# 0 = 8-15
	# 1 = 15-20
	# 2 = 20-30
	# 3 = 30-45
	# 4 = 45-55
	# 5 = 55-70
	# 6 = 70-..
	age = models.PositiveSmallIntegerField(null=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('profile', kwargs={'pk' : self.pk})

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except Exception:
			url = ''
		return url


class Category(models.Model):
	# 0 = 8-15
	# 1 = 15-20
	# 2 = 20-30
	# 3 = 30-45
	# 4 = 45-55
	# 5 = 55-70
	# 6 = 70-..
    interval = models.PositiveSmallIntegerField(null=True)
    gender = models.PositiveSmallIntegerField(null=True)
	


class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except Exception:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		orderitems = self.orderitem_set.all()
		return any(i.product.digital == False for i in orderitems)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		return sum(item.get_total for item in orderitems) 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		return sum(item.quantity for item in orderitems) 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		return self.product.price * self.quantity

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	country = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address