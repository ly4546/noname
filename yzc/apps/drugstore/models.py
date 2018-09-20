from django.db import models

# Create your models here.

from apps.Operate.models import CatenaryProduct
from apps.agent.models import PeriodTotalSale,AgentInformation

class Order(models.Model):
    drugstore_feedback_choices=(
        ('1','已收货'),
        ('2','待收货')
    )
    distributor_feedback_choices=(
        ('1',''),
        ('2',''),
        ('3',''),
        ('4',''),
    )
    is_apply_money_choices=(
        ('1','未提现'),
        ('2','申请中'),
        ('3','已打款'),
    )

    order_number = models.CharField(verbose_name='订单编号',max_length=32)
    product = models.ForeignKey(CatenaryProduct,related_name='product_information',on_delete=models.CASCADE)
    buy_unit = models.CharField(verbose_name='下单单位',max_length=32)
    buy_unit_name = models.CharField(verbose_name='下单单位名称',max_length=3)
    hang_region_code = models.CharField(verbose_name='挂网区域',max_length=12)
    hang_price = models.IntegerField(verbose_name='挂网价格',default=0, blank=True)
    buy_quantity = models.IntegerField(verbose_name='采购数量',default=0, blank=True)
    buy_time = models.DateTimeField(verbose_name='采购时间',auto_now_add=True)
    proxy = models.ForeignKey(AgentInformation,related_name='agent_order',on_delete=models.CASCADE)
    proxy_name = models.CharField(verbose_name='代理商名称',max_length=32)
    rebate_object_id = models.IntegerField(verbose_name='提成对象id',default=0, blank=True)
    rebate_object = models.CharField(verbose_name='提成对象名称',max_length=32)
    affiliation_cycle = models.CharField(verbose_name='所属周期',max_length=12)
    current_sales = models.ForeignKey(PeriodTotalSale,related_name='total_nums',on_delete=models.CASCADE)
    confirm_receipt = models.IntegerField(verbose_name='确认收货量',default=0, blank=True)
    estimated_cash = models.IntegerField(verbose_name='预计提现金额',default=0, blank=True)
    feedback = models.CharField(verbose_name='药店反馈',choices=drugstore_feedback_choices,default=2)
    receipt_time = models.DateTimeField(verbose_name='收货时间',auto_now_add=True)
    actual_order = models.IntegerField(verbose_name='实际订单量',default=0, blank=True)
    actual_cash = models.IntegerField(verbose_name='实际返利金额',default=0, blank=True)
    distributor_feedback = models.CharField(verbose_name='配送商反馈',choices=distributor_feedback_choices,default=1,max_length=12)
    confirm_time = models.DateTimeField(verbose_name='配送商确认回款时间',auto_now_add=True)
    is_apply_money = models.CharField(verbose_name='提现状态',choices=is_apply_money_choices,default=1,max_length=12)
    apply_time = models.DateTimeField(verbose_name='申请提现时间',auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = verbose_name_plural = '订单'

class ReturnOrder(models.Model):
    distributor_feedback_choices=(
        ('1',''),
        ('2',''),
        ('3',''),
    )
    backout_id = models.CharField(verbose_name='退单编号',max_length=32)
    product = models.ForeignKey(CatenaryProduct,related_name='product_information',on_delete=models.CASCADE)
    buy_unit = models.CharField(verbose_name='采购单位',max_length=32)
    refunds_numbers = models.IntegerField(verbose_name='退货数量',default=0, blank=True)
    original_order = models.ForeignKey(Order,related_name='original_order',on_delete=models.CASCADE)
    refunds_time = models.DateTimeField(auto_now_add=True)
    distributor_feedback = models.CharField(verbose_name='配送商反馈',choices=distributor_feedback_choices,default=1,max_length=1)

    class Meta:
        db_table = 'return_orders'
        verbose_name = verbose_name_plural = '退货订单'
