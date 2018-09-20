#encoding:utf-8
from django.db import models


from agent.consts import STATUS_CHOICES
# Create your models here.

class AgentInformation(models.Model):
    nick = models.CharField(verbose_name='昵称',max_length=100,blank=True)
    account = models.IntegerField(verbose_name='账号',unique=True)
    nmp_user_id = models.CharField(verbose_name='新势力user_id',max_length=100)
    mobile = models.CharField (verbose_name='联系手机号',max_length=11,unique=True)
    name = models.CharField(verbose_name='联系人姓名',max_length=36,blank=True)
    status = models.IntegerField(verbose_name='代理状态',choices=STATUS_CHOICES,max_length=1)
    creat_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    is_del = models.BooleanField(verbose_name='是否删除',default=False)

    class Meta:
        db_table = 'agents'
        verbose_name = verbose_name_plural = '代理商'

class AgentDetail(models.Model):
    user = models.ForeignKey(AgentInformation,related_name='agent_detail',on_delete=models.CASCADE)
    product = models.ForeignKey('operate.CatenaryProduct',related_name='agent_product',on_delete=models.CASCADE)
    is_del = models.BooleanField(verbose_name='是否解约',default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent_details'
        verbose_name = verbose_name_plural = '代理商详情'

class ContractRule(models.Model):
    from_nums = models.IntegerField(verbose_name='开始数量',default=0)
    end_nums = models.IntegerField(verbose_name='终止数量',default=0)
    rebate = models.FloatField(verbose_name='返利金额',default=0, blank=True)
    rule = models.ForeignKey('operate.DrugNettingArea',related_name='drug_area',on_delete=models.CASCADE)
    is_del = models.BooleanField(verbose_name='是否删除',default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contract_rules'
        verbose_name = verbose_name_plural = '签约规则'

class PeriodTotalSale(models.Model):
    product = models.ForeignKey('operate.CatenaryProduct',related_name='product',on_delete=models.CASCADE)
    hang_region_code = models.CharField(verbose_name='挂网区域',max_length=12)
    rebate_object_id = models.IntegerField(verbose_name='销售代表id')
    totail_num = models.IntegerField(verbose_name='代理该药品的销售总量',default=0)
    totail_level = models.CharField(verbose_name='销售等级',max_length=10)
    current_price = models.FloatField(verbose_name='当前配网价格',default=0)
    current_rebate = models.FloatField(verbose_name='当前提成金额',default=0)
    confirm_totail_num = models.IntegerField(verbose_name='实际代理该药品的销售总量',default=0)
    confirm_totail_level = models.CharField(verbose_name='实际销售等级',max_length=10)
    confirm_totail_rebate = models.FloatField(verbose_name='实际当前提成金额',default=0)
    current_period = models.CharField(verbose_name='当前周期',max_length=12)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'period_total_sales'
        verbose_name = verbose_name_plural = '统计周期内的销售总量'

class PharmacyRelated(models.Model):
    pharmacy_account = models.CharField(verbose_name='药店账户',max_length=32)
    pharmacy_account_id = models.CharField(verbose_name='药店id',max_length=64)
    sales_account_id = models.CharField(verbose_name='销售代表账号',max_length=32)
    product = models.ForeignKey('operate.CatenaryProduct',related_name='product',on_delete=models.CASCADE)
    proxy = models.ForeignKey(AgentInformation,related_name='agent',on_delete=models.CASCADE)
    is_del = models.BooleanField(verbose_name='是否解绑',default=False)
    status = models.BooleanField(verbose_name='是否自动升级',default=False)
    is_apply = models.BooleanField(verbose_name='销售代表是否主动申请',default=False)
    sales = models.ForeignKey(PeriodTotalSale,related_name='period_sale_totail',on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pharmacy_related'
        verbose_name = verbose_name_plural = '药店相关'
