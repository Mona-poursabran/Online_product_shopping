from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixin import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime
import json

def success_login(req):
    if req.user.is_superuser:
        return redirect('admin_panel')
    else:
        return redirect('store')

def store(req): 
    product = Product.objects.all()
    context={'products': product}
    return render(req, 'store/store.html', context)


def cart(req):
    if req.user.is_authenticated:
        customer = req.user
        order, create = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem.all()
        print('items:', items)
    else:
        items =[]
        order = {'get_cart_items':0, 'get_cart_total':0}
    context={'items': items, 'order':order}
    return render(req, 'store/cart.html',context)


def checkout(req):
    if req.user.is_authenticated:
            customer = req.user
            order, create = Order.objects.get_or_create(customer=customer, complete = False)
            items = order.orderitem.all()
            print('items:', items)    
    else:
        items =[]
        order = {'get_cart_items':0, 'get_cart_total':0}
    context={'items': items, 'order':order}
    return render(req, 'store/checkout.html', context)


def updateitem(requset):
    data = json.loads(requset.body)
    productId = data['productId']
    action = data['action']
    print('data', data)
    print('productId', productId)
    print('action', action)

    customer = requset.user
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer=customer, complete = False)
    orderitem, create = OrderItem.objects.get_or_create(order= order, product= product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transitionid = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated :
        customer = request.user
        order, create = Order.objects.get_or_create(customer=customer, complete = False)
        total = data['form']['total']
        order.transaction_id = transitionid
        if int(total) == int(order.get_cart_total) :
            order.complete = True
        order.save()

        address = Address.objects.create(customer= customer,
                                           order = order, 
                                           address = data['Information']['address'], 
                                           city =data['Information']['city'],
                                           street =data['Information']['street'],
                                           plaque =data['Information']['plaque'])
    else :
        print('user is not logged in')
    return JsonResponse('payment submitted...', safe=False)



# class ViewDetail(DetailView):
#     model= Product
#     template_name='store/view_product.html'



##################### Admin Panel ########################

class AdminPanel (SuperUserRequiredMixin,LoginRequiredMixin, TemplateView ):
    template_name = 'store/admin_panel.html'


class ProductsList(SuperUserRequiredMixin,LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'


class CreateProduct(SuperUserRequiredMixin,LoginRequiredMixin, CreateView):
    model = Product
    template_name="store/new_product.html"
    fields= '__all__'
    success_url = reverse_lazy('product_list')

    # def post(self, request, *args, **kwargs) :
    #     name= request.POST.get('name')
    #     price= request.POST.get('price')
    #     image= request.POST.get('image')
    #     digital= request.POST.get('digital')
        
    #     form = self.get_form()
    #     if form.is_valid():
    #         new = Product.objects.create(name= name, price= price, image= image, digital= digital)
    #         return redirect('product_list')
    #     else:
    #         return self.form_invalid(form)


class ProductDetail(SuperUserRequiredMixin,LoginRequiredMixin, DetailView):
    model = Product
    template_name='store/product_detail.html'
    


class UpdateProduct(SuperUserRequiredMixin,LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'store/update_pro.html'
    fields = "__all__"
    success_url = reverse_lazy('product_list')



class DeleteProduct(LoginRequiredMixin, View):
       def get(self,request, pk, *args, **kwargs):
        if request.is_ajax:
            food = Product.objects.get(pk = pk)
            food.delete()
            return JsonResponse({"message": "success"})
        return JsonResponse({"message":"wrong"})





############# Search ###################

def search_result(req):
    """
        all users are able to search products' name with ajax
    """
    if req.is_ajax():
        res = None
        result = req.POST.get('data')
        q = Product.objects.filter(name__icontains= result)
      
        if len(q) > 0 and len(result) > 0:
            data =[]
            for i in q:
                item ={
                    'pk' : i.pk,
                    'name':i.name,
                    'image': i.image.url,
                    'price': i.price,
                    'digital': i.digital
                }
                data.append(item)
            res = data
           
        else:
            res = "No Product Found..."

        return JsonResponse({'dataa':res})
    return JsonResponse({})



def get_info_search(req, pk):
    obj = get_object_or_404(Product, pk=pk)
    return render(req, 'store/search.html', {'obj':obj})