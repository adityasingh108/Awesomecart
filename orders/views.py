from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from carts.models import Cart,CartItem
from .forms import OrderForm
from .models import Order
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



# Create your views here.

def payments(request):
    # get the data from the payapal in format of json 
    body = json.loads(request.body)
    print(body)
    # SAVE THE TRANSACTION DATA IN THE DATBSAE
    order = Order.objects.get(user = request.user,is_ordered =False, order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method= body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    
    # MOVE ITEM TO THE PRODUCT TABLE 
    
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id  = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered= True
        orderproduct.save()
         
        #  variation of the cart item  saved
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
    # DECREMENT THE SOLD ITEMS FROM THE DATABASE
        product = Product.objects.get(id=item.product_id)
        product.stock -=item.quantity
        product.save()
    
    #  CLEAR THE CART
    CartItem.objects.filter(user=request.user).delete()
    
    # SEND ORDER RECIVED THE TO THE USER EMAIL 
    mail_subject = 'Thanku for your order'
    message = render_to_string('orders/order_complete_mail.html',{
        'user':request.user,
        'order':order,
        
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    
    # SEND THE ORDER ID AND TRANSACTION ID TO sendData VIA JSON RESPOSE 
    
    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }
    
    return JsonResponse(data)

def place_order(request,total = 0,quantity = 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user= current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    GrandTotal = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    tax = (2 *total)/100
    GrandTotal = total+tax    

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']    
            data.last_name = form.cleaned_data['last_name']    
            data.phone = form.cleaned_data['phone']    
            data.email = form.cleaned_data['email']    
            data.address_line_1 = form.cleaned_data['address_line_1']    
            data.address_line_2 = form.cleaned_data['address_line_2']    
            data.country = form.cleaned_data['country']    
            data.state = form.cleaned_data['state']    
            data.city = form.cleaned_data['city']    
            data.order_note = form.cleaned_data['order_note']
            data.order_total = GrandTotal
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context= {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'GrandTotal':GrandTotal
            }
            
            return render(request ,'orders/payments.html',context)
        else:
            return redirect('checkout')
        
        
        
        
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_product =OrderProduct.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id = transID)
        
        subtotal = 0
        for i in ordered_product:
            subtotal = i.product_price * i.quantity
        context = {
            'order':order,
            'ordered_product':ordered_product,
            'order_number':order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'orders/order_complete.html',context)   
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('Home')     
               
               
    

    