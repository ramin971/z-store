import logging
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.shortcuts import render,get_object_or_404,redirect
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from core.models import Cart,Size
import uuid

def go_to_gateway_view(request):
# def go_to_gateway_view(request,*args,**kwargs):

    # خواندن مبلغ از هر جایی که مد نظر است
    # amount = kwargs['price']
    # user_mobile_number = kwargs['mobile']
    # cart_id = kwargs['id']
    # print('###########')

    amount = request.session.get('price')
    user_mobile_number = request.session.get('mobile')
    cart_id = uuid.UUID(request.session.get('id'))
    print('###########')
    print('@@@@id,mobile,price',cart_id,user_mobile_number,amount)
    print('@@@@',type(cart_id),type(user_mobile_number),type(amount))

    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    # user_mobile_number = request.POST.get('mobile')  # اختیاری
    # cart_id = request.POST.get('id')
    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        # bank.set_client_callback_url(reverse("callback-gateway", kwargs={'cart_id':cart_id}))
        bank.set_client_callback_url(reverse("callback-gateway"))

        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e
    


def callback_gateway_view(request):
# def callback_gateway_view(request,*args,**kwargs):

    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        print('suuuuuuuuuuuuuccesssssssssssss')
        cart_id = uuid.UUID(request.session.get('id'))
        del request.session['price']
        del request.session['mobile']
        del request.session['id']

        cart = get_object_or_404(Cart,id=cart_id)
        cart.payment = True
        # cart.tracking_code = kwargs['tc']
        cart.save()
        for order in cart.ordre_items.all():
            size = get_object_or_404(Size,id=order.size)
            size.stock = size.stock - order.quantity
            size.save()
            
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        # return HttpResponse("پرداخت با موفقیت انجام شد.")
        return redirect(reverse('receipt',kwargs={'tc':tracking_code,'cart_id':cart_id}))

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )













