from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
import jdatetime

# class Customer(models.Model):
#     user = models.OneToOneField(User, null= True, blank=True, on_delete=models.CASCADE)
#     def __str__(self) -> str:
#         return str(self.user.username)
    
class Product(models.Model):
    name=models.CharField(max_length=200, null= True)
    image = models.ImageField(upload_to='items/%Y_%m_%d', null= True, blank=True)
    price = models.IntegerField()
    digital = models.BooleanField(default= False, null= True, blank=False)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer= models.ForeignKey(User, on_delete=models.SET_NULL, null= True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False, null= True, blank=True)
    transaction_id = models.CharField(max_length=100, null= True)
    
    @property 
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(datetime= self.date_ordered)
    
    def __str__(self) -> str:
        return f'{self.customer} {str(self.id)}'

    @property
    def get_cart_items(self):
        orderitems =self.orderitem.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    @property
    def get_cart_total(self):
        orderitems= self.orderitem.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def delivery(self):
        delivery = False
        orderitems = self.orderitem.all()
        for item in orderitems:
            if item.product.digital == False:
                delivery = True
        return delivery



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null= True, related_name='orderitem_p')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null = True, related_name='orderitem')
    quantity= models.IntegerField(default=0, null= True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product.name)
    
    
    @property 
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(datetime= self.date_created)
    
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Address(models.Model):
    customer= models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null= True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    plaque = models.IntegerField(validators=[MinValueValidator(0)])
    date_created = models.DateTimeField(auto_now_add=True)


    @property 
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(datetime= self.date_created)
    
    
    def __str__(self) -> str:
        return self.address


