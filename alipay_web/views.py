# !/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import datetime
import pytz

from alipay_web.utils.sdk.alipay import AliPay

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .conf import conf
from . import models

APPID = conf.appid
APP_PRIVATE_KEY_PATH = conf.app_private_key_path
ALI_PUBLIC_KEY_PATH = conf.ali_pub_key_path
ALI_GATEWAY = conf.alipay_gateway
pre_url = conf.callback_pre_url

CHINA_ZONE = pytz.timezone('Asia/Shanghai')


# 生成Alipay对象函数
def alipay():
    obj = AliPay(
        appid=APPID,
        app_notify_url=pre_url + reverse(viewname='pay_notify'),  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        return_url=pre_url + reverse(viewname='pay_result'),  # 如果支付成功，重定向回到你的网站的地址。
        alipay_public_key_path=ALI_PUBLIC_KEY_PATH,  # 支付宝公钥
        app_private_key_path=APP_PRIVATE_KEY_PATH,  # 应用私钥
        debug=True,  # 默认False, 是否使用沙箱环境
    )
    return obj


# 结算订单视图：生成订单，重定向支付宝收银台页面
def pay_order(request):
    if request.method == 'GET':
        return render(request, 'pay.html')  # 结算页面

    money = request.POST.get('money')
    money = float(money)

    # 生成待支付订单
    user = models.Account.objects.get(pk=1)  # 这里demo写死；实际应该根据业务而定
    order_obj = models.Order.objects.create(payment_type=1, order_number=str(uuid.uuid4()), account=user,
                                            actual_amount=money, status=1)
    # 购买商品描述
    product_list = ['Python全栈课程24个月', 'Linux运维']

    suject_title = ';'.join(product_list)
    order_id = order_obj.order_number

    # 根据订单信息，生成重定向url
    pay_obj = alipay()
    print(pay_obj.app_notify_url, pay_obj.return_url)
    query_params = pay_obj.direct_pay(subject=suject_title,
                                      out_trade_no=order_id,
                                      total_amount=money)
    pay_url = pay_obj.gateway + '?' + query_params
    # print(pay_url)
    return redirect(to=pay_url)


# 异步回调，修改订单状态视图
def async_notify(request):
    """
    回调是POST请求
    参数分为公共参数和业务参数
    参数详情列表参考：https://docs.open.alipay.com/270/105902/
    """
    infos = request.POST.dict()  # 获取请求信息已字典的形式
    print('回到参数：', infos)
    sign_str = infos.pop('sign')
    pay_obj = alipay()
    verify_sign_status = pay_obj.verify(infos, signature=sign_str)
    if verify_sign_status:
        print('异步回调验签成功')
        # 验签成功,修改订单
        trade_status = infos.get('trade_status')
        out_trade_no = infos.get('out_trade_no')
        ali_trade_no = infos.get('trade_no')
        appid = infos.get('app_id')

        if appid != APPID:
            print('appid错误！')
            return HttpResponse('failure')

        try:
            order_obj = models.Order.objects.get(order_number=out_trade_no)
        except ObjectDoesNotExist as e:
            print('订单号不存在！')
            return HttpResponse('failure')  # 订单不存在

        if order_obj.status != 1:  # 表示订单已经不是待支付状态.(订单已支付或订单取消等)
            print('订单状态已不是待支付！')
            return HttpResponse('failure')

        if order_obj.actual_amount != float(infos.get('total_amount')):
            return HttpResponse('failure')

        if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':  # 支付成功
            order_obj.payment_number = ali_trade_no
            order_obj.status = 0
            order_obj.pay_time = datetime.datetime.now(CHINA_ZONE)
            order_obj.save()

            return HttpResponse('success')
    return HttpResponse('failure')


def pay_result(request):
    data = request.GET.dict()
    print('同步回调参数:', data)
    sign = data.pop('sign')
    alipay_obj = alipay()
    verify_status = alipay_obj.verify(data, signature=sign)
    if verify_status:
        return HttpResponse('支付成功！')
    # return redirect(to='http://www.baidu.com')
    return HttpResponse('验签失败！异常支付！')
