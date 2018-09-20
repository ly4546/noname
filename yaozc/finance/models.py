#encoding:utf-8
from django.db import models


from finance.consts import  STATUS_CHOICES

# Create your models here.


class FinanceCash(models.Model):

    Put_Forward_number = models.CharField(verbose_name='提现编号',max_length=32)
    order_uid = models.ForeignKey('drugstore.Order',related_name='order',on_delete=models.CASCADE)
    apply_alipay = models.CharField(verbose_name='提现账户',max_length=64)
    confirm_time = models.DateTimeField(verbose_name='提现确认时间',null=True, blank=True)
    status = models.CharField(verbose_name='状态',choices=STATUS_CHOICES,default=1,max_length=1)
    remarks = models.CharField(verbose_name='备注',max_length=256,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finance_cashs'
        verbose_name = verbose_name_plural = '财务提现'

