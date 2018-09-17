from django.db import models

# Create your models here.

from apps.DrugStore.models import Order


class FinanceCash(models.Model):
    status_choices = (
        ('1',''),
        ('2',''),
        ('3',''),
        ('4',''),
    )
    order_uid = models.ForeignKey(Order,related_name='order',on_delete=models.CASCADE)
    apply_alipay = models.CharField(verbose_name='提现账户',max_length=64)
    confirm_time = models.DateTimeField(auto_now=True)
    status = models.CharField(verbose_name='状态',choices=status_choices,default=1,max_length=1)
    remarks = models.CharField(verbose_name='备注',max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'finance_cashs'
        verbose_name = verbose_name_plural = '财务提现'

