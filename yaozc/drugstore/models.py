#encoding:utf-8
from django.db import models



from drugstore.consts import DISTRIBUTOR_FEEDBACK_CHOICES,DRUGSTORE_FEEDBACK_CHOICES,\
                             IS_APPLY_MONEY_CHOICES,PAY_METHOD_WAY,ORDER_STATUS,PAY_STATUS
# Create your models here.

class Order(models.Model):
    order_number = models.CharField(verbose_name='订单编号',max_length=32)
    product = models.ForeignKey('operate.CatenaryProduct',related_name='product_information',on_delete=models.CASCADE)
    buy_unit = models.CharField(verbose_name='下单单位',max_length=32)
    buy_unit_name = models.CharField(verbose_name='下单单位名称',max_length=3)
    hang_region_code = models.CharField(verbose_name='挂网区域',max_length=12)
    hang_price = models.FloatField(verbose_name='挂网价格',default=0)
    buy_quantity = models.IntegerField(verbose_name='采购数量',default=1)
    buy_time = models.DateTimeField(verbose_name='采购时间')
    proxy = models.ForeignKey('agent.AgentInformation',related_name='agent_order',on_delete=models.CASCADE)
    proxy_name = models.CharField(verbose_name='代理商名称',max_length=32)
    rebate_object_id = models.IntegerField(verbose_name='提成对象id',blank=True)
    rebate_object = models.CharField(verbose_name='提成对象名称',max_length=32)
    affiliation_cycle = models.CharField(verbose_name='所属周期',max_length=8)
    current_sales = models.ForeignKey('agent.PeriodTotalSale',related_name='total_nums',on_delete=models.CASCADE)
    confirm_receipt = models.IntegerField(verbose_name='确认收货量',default=0)
    estimated_cash = models.FloatField(verbose_name='预计提现金额',default=0)
    feedback = models.IntegerField(verbose_name='药店反馈',choices=DRUGSTORE_FEEDBACK_CHOICES,default=2)
    receipt_time = models.DateTimeField(verbose_name='收货时间')
    actual_order = models.IntegerField(verbose_name='实际订单量',default=0)
    actual_cash = models.FloatField(verbose_name='实际返利金额',default=0)
    distributor_feedback = models.IntegerField(verbose_name='配送商反馈',choices=DISTRIBUTOR_FEEDBACK_CHOICES,default=1,max_length=12)
    confirm_time = models.DateTimeField(verbose_name='配送商确认回款时间',null=True, blank=True)
    is_apply_money = models.IntegerField(verbose_name='提现状态',choices=IS_APPLY_MONEY_CHOICES,default=1,max_length=12)
    apply_time = models.DateTimeField(verbose_name='申请提现时间',null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    pay_method_way = models.IntegerField(verbose_name='支付方式',choices=PAY_METHOD_WAY)
    pay_method_type = models.IntegerField(verbose_name='支付类型',null=True,blank=True)
    order_status = models.IntegerField(verbose_name='订单状态',choices=ORDER_STATUS)
    pay_status = models.IntegerField(verbose_name='支付状态',choices=PAY_STATUS)
    is_finish = models.BooleanField(verbose_name='订单是否结束',default=False)

    class Meta:
        db_table = 'orders'
        verbose_name = verbose_name_plural = '订单'

class ReturnOrder(models.Model):
    distributor_feedback_choices=(
        ('1',''),
        ('2',''),
        ('3',''),
    )
    backout_number = models.CharField(verbose_name='退单编号',max_length=32)
    product = models.ForeignKey('operate.CatenaryProduct',related_name='product_information',on_delete=models.CASCADE)
    buy_unit = models.CharField(verbose_name='采购单位',max_length=32)
    refunds_numbers = models.IntegerField(verbose_name='退货数量',default=1)
    original_order = models.ForeignKey(Order,related_name='original_order',on_delete=models.CASCADE)
    refunds_time = models.DateTimeField(verbose_name='退货时间',auto_now=True)
    distributor_feedback = models.CharField(verbose_name='配送商反馈',choices=distributor_feedback_choices,default=1,max_length=1)
    reason = models.TextField(verbose_name='退货原因',blank=True,null=True)
    is_success = models.BooleanField(verbose_name='申请退货是否成功',default=False)
    reject_reason = models.TextField(verbose_name='申请退货不成功原因')

    class Meta:
        db_table = 'return_orders'
        verbose_name = verbose_name_plural = '退货订单'
