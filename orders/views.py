from cart.views import get_cart, cart_clear
from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from . import Checksum
from .models import OrderItem, Order, Product
from .forms import OrderCreatedForm
from orders.utils import VerifyPaytmResponse

def order_create(request):
    """ Creates order and attaches payment details """
    cart = get_cart(request)

    if request.method == 'POST':
        order_form = OrderCreatedForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data

            # Save order details
            order = order_form.save(commit=False)
            # If user is authenticated save order details to user
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Get Products
            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)

            # Add products to order
            for product in products:
                cart_item = cart[str(product.id)]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )

            # Get Payment Gateway Credentials
            data_dict = {
                'MID': settings.PAYTM_MERCHANT_ID,
                'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
                'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
                'MOBILE_NO': data['mobile'],
                'EMAIL': data['email'],
                'CUST_ID': '123123',
                'ORDER_ID':str(order.id),
                'TXN_AMOUNT': str(order.get_total_cost()),
            }
            data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
            context = {
                'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
                'comany_name': settings.PAYTM_COMPANY_NAME,
                'data_dict': data_dict
            }
            
            # Clear cart and goto payments page
            cart_clear(request)
            return render(request, 'payment.html', context)
    else:
        order_form = OrderCreatedForm()
        if request.user.is_authenticated:
            # Fill the form with default profile details
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'mobile': request.user.profile.phone_number,
                'address': request.user.profile.address,
                'postal_code': request.user.profile.postal_code,
                'city': request.user.profile.city,
                'country': request.user.profile.country,
            }
            order_form = OrderCreatedForm(initial=initial_data)
        return render(
            request,
            'order_create.html',
            {
                'cart': cart,
                'order_form': order_form,
            }
        )

def order_detail(request, order_id):
    """ Displays order details """
    order = Order.objects.get(pk=order_id)
    return render(
        request,
        'order_detail.html',
        {'order': order}
    )


@csrf_exempt
def callback(request):
    """ Handles the post tasks after payment """
    if request.method == 'POST':
        received_data = dict(request.POST)
        # If payment is not successful cancel order
        if received_data['STATUS'][0] != 'TXN_SUCCESS':
            order_id = int(received_data['ORDERID'][0])
            order = Order.objects.get(pk=order_id)
            order.status = 'Payment Failed'
            order.save()
        
        # # Verify Payment 
        # paytm_params = {}
        # paytm_checksum = received_data['CHECKSUMHASH'][0]
        # for key, value in received_data.items():
        #     if key == 'CHECKSUMHASH':
        #         paytm_checksum = value[0]
        #     else:
        #         paytm_params[key] = str(value[0])
        # # Verify checksum
        # is_valid_checksum = Checksum.verify_checksum(paytm_params, settings.PAYTM_MERCHANT_KEY, str(paytm_checksum))
        # if is_valid_checksum:
        #     received_data['message'] = "Checksum Matched"
        # else:
        #     received_data['message'] = "Checksum Mismatched"
        #     return render(request, 'callback.html', context=received_data)
        # return render(request, 'callback.html', context=received_data)
        return redirect('/users/profile/')