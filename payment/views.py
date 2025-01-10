
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404,redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from azbankgateways import (
#     bankfactories,
#     models as bank_models,
#     default_settings as settings,
# )
# from azbankgateways.exceptions import AZBankGatewaysException
from core.models import Cart,Size
from core.serializers import CartDetailSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Main
from idpay.api import IDPayAPI


# def go_to_gateway_view(request):
# # def go_to_gateway_view(request,*args,**kwargs):

#     # خواندن مبلغ از هر جایی که مد نظر است
#     # amount = kwargs['price']
#     # user_mobile_number = kwargs['mobile']
#     # cart_id = kwargs['id']
#     # print('###########')

#     amount = request.session.get('price')
#     user_mobile_number = request.session.get('mobile')
#     cart_id = uuid.UUID(request.session.get('id'))
#     print('###########')
#     print('@@@@id,mobile,price',cart_id,user_mobile_number,amount)
#     print('@@@@',type(cart_id),type(user_mobile_number),type(amount))

#     # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
#     # user_mobile_number = request.POST.get('mobile')  # اختیاری
#     # cart_id = request.POST.get('id')
#     factory = bankfactories.BankFactory()
#     try:
#         bank = (
#             factory.auto_create()
#         )  # or factory.create(bank_models.BankType.BMI) or set identifier
#         bank.set_request(request)
#         bank.set_amount(amount)
#         # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
#         # bank.set_client_callback_url(reverse("callback-gateway", kwargs={'cart_id':cart_id}))
#         bank.set_client_callback_url(reverse("callback-gateway"))

#         bank.set_mobile_number(user_mobile_number)  # اختیاری
    
#         # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
#         # پرداخت برقرار کنید.
#         bank_record = bank.ready()

#         # هدایت کاربر به درگاه بانک
#         return bank.redirect_gateway()
#     except AZBankGatewaysException as e:
#         logging.critical(e)
#         # redirect to failed page.
#         raise e
    


# def callback_gateway_view(request):
# # def callback_gateway_view(request,*args,**kwargs):

#     tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
#     if not tracking_code:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     try:
#         bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
#     except bank_models.Bank.DoesNotExist:
#         logging.debug("این لینک معتبر نیست.")
#         raise Http404

#     # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
#     if bank_record.is_success:
#         print('suuuuuuuuuuuuuccesssssssssssss')
#         cart_id = uuid.UUID(request.session.get('id'))
#         del request.session['price']
#         del request.session['mobile']
#         del request.session['id']

#         cart = get_object_or_404(Cart,id=cart_id)
#         cart.payment = True
#         # cart.tracking_code = kwargs['tc']
#         cart.save()
#         for order in cart.ordre_items.all():
#             size = get_object_or_404(Size,id=order.size)
#             size.stock = size.stock - order.quantity
#             size.save()

#         # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
#         # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
#         # return HttpResponse("پرداخت با موفقیت انجام شد.")
#         return redirect(reverse('receipt',kwargs={'tc':tracking_code,'cart_id':cart_id}))

#     # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
#     return HttpResponse(
#         "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
#     )


# def go_to_pay_view(request):
#     amount = request.session.get('price')
#     user_mobile_number = request.session.get('mobile')
#     cart_id = request.session.get('id')
#     call_back_url = reverse("callback-pay")
#     my_data ={
#         "amount": int(amount),
#         "callback": str(call_back_url),
#         "desc": "Hello World!",
#         "order_id": cart_id,
#         "phone": str(user_mobile_number)
#     }
#     # print('###########')
#     # print('@@@@id,mobile,price',cart_id,user_mobile_number,amount)
#     # print('@@@@',type(cart_id),type(user_mobile_number),type(amount))
#     final_data = requests.post('https://api.idpay.ir/v1.1/payment',headers={'Content-Type':'application/json','X-API-KEY':'6a7f99eb-7c20-4412-a972-6dfb7cd253a4','X-SANDBOX':'1'}, data={})
#     print('this line ????????????????????????????')
#     print(final_data.status_code)
#     # print(final_data)
#     print(final_data.json())

#     # return redirect(reverse("callback-pay",kwargs={'tc':final_data['trackId'],'result':final_data['result']}))

#     return redirect(reverse("callback-pay",kwargs={'id':final_data['id'],'link':final_data['link']}))
#     # return final_data

# def callback_pay_view(request,*args,**kwargs):
#     print('call back**********************')
#     cart_id = uuid.UUID(request.session.get('id'))

#     # result = request.GET.get('result', None)
#     result = kwargs['result']
#     if result is None:
#         print('*********not result')
#         raise Http404
#     if result == 100:
#         # tracking_code = request.GET.get('trackId')
#         tracking_code = kwargs['trackId']
#         print('#####tc',tracking_code)
#         cart = get_object_or_404(Cart,id=cart_id)
#         cart.payment = True
#         # cart.tracking_code = kwargs['tc']
#         cart.save()
#         for order in cart.ordre_items.all():
#             size = get_object_or_404(Size,id=order.size)
#             size.stock = size.stock - order.quantity
#             size.save()
#         return redirect(reverse('receipt',kwargs={'tc':tracking_code,'cart_id':cart_id}))

#     return HttpResponse(
#         "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
#     )



def payment_init():
    # base_url = config('BASE_URL', default='http://127.0.0.1', cast=str)
    # api_key = config('IDPAY_API_KEY', default='', cast=str)
    # sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)
    base_url = 'http://127.0.0.1:8000'
    # base_url = 'https://your-domain.com'
    api_key = '6a7f99eb-7c20-4412-a972-6dfb7cd253a4'
    sandbox = 1
    return IDPayAPI(api_key, base_url, sandbox)


@api_view(['GET'])
def payment_start(request):
    if request.method == 'GET':

        order_id = request.session.get('id')
        amount = request.session.get('price')
        user_mobile_number = request.session.get('mobile')
        call_back_url = reverse("payment_return")
        payer = {
            'phone': user_mobile_number,
        }
        # print('#####amount: ',amount)
        if order_id is None or amount is None:
            raise Http404
        record = Main(order_id=order_id, amount=int(amount))
        record.save()

        idpay_payment = payment_init()
        result = idpay_payment.payment(str(order_id), amount, call_back_url, payer)

        if 'id' in result:
            # print('######## id in result :',result)
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
            # print('######## id not in result :',txt)
    else:
        txt = "Bad Request"
        # print('###### bad request')

    return Response({'message' : txt})

@api_view(['POST'])
@csrf_exempt
def payment_return(request):
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')
        print(pid,' # ',status,' # ',pidtrack,' # ',order_id,' # ',amount,' # ',card,' # ',date)

        if Main.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()

            payment = Main.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()
            # print('#######str status',str(status))
            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:
                    print('####status in result')
                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()
                    # print('####result status',result['status'])

                    if result['status'] == 100:
                        cart = get_object_or_404(Cart,id=order_id)
                        cart.payment = True
                        cart.status = 'queue'
                        # cart.tracking_code = kwargs['tc']
                        cart.save()

                        for order in cart.order_items.all():
                            size = get_object_or_404(Size,id=order.size.id)
                            size.stock = size.stock - order.quantity
                            size.save()
                        # print('*****message******',result['message'])
                        return redirect(reverse('receipt',kwargs={'tc':pidtrack,'cart_id':order_id}))
                    return  Response({'message' : result['message']})

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return Response({'message' : txt})



@api_view(['GET'])
def receipt(request,*args,**kwargs):
    cart = get_object_or_404(Cart,id=kwargs['cart_id'])
    serializer = CartDetailSerializer(cart,context={'request':request})
    response = serializer.data
    response['tracking_code'] = kwargs['tc']
    if 'price' in request.session:
        del request.session['price']
        del request.session['mobile']
        del request.session['id']

    return Response(response,status=status.HTTP_200_OK)

