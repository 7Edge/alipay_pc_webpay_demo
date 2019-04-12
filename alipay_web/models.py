import hashlib

from django.db import models

# Create your models here.
"""
demo演示一个在线教育系统的购买支付。涉及到的models如下：
订单表
订单详情表
"""


# 23 账号表
class Account(models.Model):
    """
    账号
    """
    uid = models.CharField(verbose_name='唯一ID', max_length=255, help_text='用户名的md5值,不用填写', unique=True, blank=True)

    class Meta:
        verbose_name_plural = '203. 账户表'

    def __str__(self):
        return str(self.uid)

    # 创建用户是，自动生成uid在保存用户时
    def save(self, *args, **kwargs):
        if not self.pk:
            md5_obj = hashlib.md5()
            md5_obj.update(self.uid.encode(encoding='utf8'))
            self.uid = md5_obj.hexdigest()
        super().save(*args, **kwargs)


# 38 订单表
class Order(models.Model):
    """订单"""
    payment_type_choices = ((0, '微信'), (1, '支付宝'), (2, '优惠码'), (3, '贝里'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices)

    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)
    order_number = models.CharField(max_length=128, verbose_name="订单号", unique=True)  # 考虑到订单合并支付的问题
    account = models.ForeignKey(to="Account", verbose_name='账号', on_delete=models.CASCADE)
    actual_amount = models.FloatField(verbose_name="实付金额")

    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")

    class Meta:
        verbose_name_plural = "70000001. 订单表"

    def __str__(self):
        return "%s" % self.order_number
