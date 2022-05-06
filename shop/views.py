import imp
import ast
from math import ceil
from unicodedata import category
from urllib import response
from django.shortcuts import render
from .models import Orders, Product, Contact, OrderUpdate
from django.http import HttpResponse
import json

def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    #params = {'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    #allProds = [[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query,item):
    # return true is query matches the item
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod)!=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds,'msg':""}
    if len(allProds)==0:
        params = {'msg':"Please make sure to enter relevant search query!"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    msg = {'msg': 'd-none'}
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        msg = {'msg': 'd-grid'}
    return render(request, 'shop/contact.html', msg)


def tracker(request):
    params = {'msg':'d-none'}
    if request.method == 'POST':
        OrderId = request.POST.get('OrderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=OrderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=OrderId)
                item_json = order[0].items_json
                item = ast.literal_eval(item_json)
                params ={'range':len(update),'orders':item,'update':update,'msg':'d-none'}
                return render(request,'shop/tracker.html',params) 
            else:
                params = {'msg':'d-grid'}
                return render(request,'shop/tracker.html',params)
        except Exception as e:
            pass
    return render(request, 'shop/tracker.html',params)


def prodView(request, myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    thank = False
    id = -1
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " "+request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        thank = True
        order = Orders(name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, items_json=items_json,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed!")
        update.save()
        id = order.order_id
        order.save()
    return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
