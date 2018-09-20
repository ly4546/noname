#encoding:utf-8
import os
import uuid
from datetime import datetime


from django.db import models
from django.conf import settings


from operate.consts import HANG_TYPE_CHOICES,BUY_METHOD_CHOICES,PAY_METHOD_CHOICES
# Create your models here.

class CatenaryProduct(models.Model):

    material_name = models.CharField(verbose_name='药品名称',max_length=100)
    specification = models.CharField(verbose_name='药品规格',max_length=30)
    #基础数据库信息保存在本地
    product_enterprise = models.CharField(verbose_name='生产企业',max_length=50)
    reg_number = models.CharField(verbose_name='批准文号',max_length=80)
    drug_remarks = models.CharField(verbose_name='药品备注',max_length=255,default='')
    drug_uid = models.IntegerField(verbose_name='基础数据库药品id')

    hang_license = models.CharField(verbose_name='挂网企业营业执照号',max_length=64)#以此内容去网签查询企业信息
    hang_enterprise_is_auth = models.BooleanField(verbose_name='挂网企业是否认证',default=True)
    hang_enterprise = models.CharField(verbose_name='挂网企业名称',max_length=32)#做数据库保存 当下次搜索保存时更新公司名称
    hang_type = models.IntegerField(verbose_name='挂网企业类型',choices=HANG_TYPE_CHOICES)

    hang_region_code = models.CharField(verbose_name='挂网地区',max_length=8)
    is_del = models.BooleanField(verbose_name='是否下架',default=False)
    #挂网产品属性设置
    min_unit = models.CharField(verbose_name='最小采购单位',max_length=4,null=True,blank=True)
    buy_method = models.IntegerField(verbose_name='购买形式',choices=BUY_METHOD_CHOICES,max_length=1,null=True,blank=True)
    buy_base = models.IntegerField(verbose_name='采购基数',default=1)
    is_whole = models.BooleanField(verbose_name='是否整件',default=False)
    whole_nums = models.IntegerField(verbose_name='整件数量',default=1)
    validity_time_from = models.DateTimeField(verbose_name='有效期起',null=True,blank=True)
    validity_time_end = models.DateTimeField(verbose_name='有效期止',null=True,blank=True)
    suggest_price = models.FloatField(verbose_name='建议零售价',null=True,blank=True)
    inventory = models.IntegerField(verbose_name='库存量',null=True,blank=True)
    remarks = models.CharField(verbose_name='备注说明',max_length=255,null=True,blank=True)
    content = models.TextField(verbose_name='商品描述',null=True,blank=True)
    product_type = models.CharField(verbose_name='商品分类',max_length=255,null=True,blank=True)
    total_nums = models.IntegerField(verbose_name='升级唯一代表考核数',default=500)
    pay_method = models.CharField(verbose_name='支付方式',max_length=1,choices=PAY_METHOD_CHOICES)

    class Meta:
        db_table = 'catenary_Products'
        verbose_name = verbose_name_plural = '挂网产品表'


class Distributor(models.Model):
    name = models.CharField(verbose_name='配送商名称',max_length=32)
    is_del = models.BooleanField(verbose_name='是否删除',default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'distributor'
        verbose_name = verbose_name_plural = '配送商'


class DrugNettingArea(models.Model):
    hang_region_code = models.CharField(verbose_name='挂网区域',max_length=8)
    distributor = models.ForeignKey(Distributor,related_name='distributor_area',on_delete=models.DO_NOTHING)
    hang_price = models.FloatField(verbose_name='挂网价格')
    is_del = models.BooleanField(verbose_name='是否删除',default=False)
    user = models.ForeignKey('agent.AgentInformation',related_name='agent_area',on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(CatenaryProduct,related_name='product_area',on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drug_netting_area'
        verbose_name = verbose_name_plural = '药品挂网区域'

def get_file_path(instance, filename):
    folder = instance.__class__.__name__.lower() + datetime.now().strftime("/%Y/%m/%d")
    full_folder = settings.MEDIA_ROOT + folder
    if not os.path.exists(full_folder):
        os.makedirs(full_folder)
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(full_folder, filename)


class DrugNettingPicture(models.Model):
    product = models.ForeignKey(CatenaryProduct,related_name='product_name',on_delete=models.CASCADE)
    file = models.ImageField(verbose_name='文件路径', upload_to=get_file_path)
    name = models.CharField(verbose_name='图片名称',max_length=64,blank=True)
    create_time = models.DateTimeField(verbose_name='上传时间')
    is_del = models.BooleanField(verbose_name='是否删除',default=False)

    class Meta:
        db_table = 'drug_netting_pictures'
        verbose_name = verbose_name_plural = '药品挂网图片'


class ClassificationManagement(models.Model):
    type_name = models.CharField(verbose_name='类目名称',max_length=12)
    parent = models.ForeignKey('self', verbose_name=u'上级分类', null=True, blank=True
                               ,on_delete=models.CASCADE)  # 最多二
    is_del = models.BooleanField(verbose_name='是否删除',default=False)
    un_id = models.CharField(verbose_name='唯一标识',max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drug_classification_manage'
        verbose_name = verbose_name_plural = '药品分类管理'

