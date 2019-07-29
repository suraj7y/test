from django.db import models
from currency.models import Currency

# Create your models here.

class Productmaster(models.Model):
    pro_bo_id = models.IntegerField(null=True)
    pro_name = models.CharField(max_length=500,null=True)
    pro_bo_sku = models.CharField(max_length=250,null=True)
    pro_cat_id = models.IntegerField(null=True)
    pro_brand = models.CharField(max_length=250,null=True)
    pro_price = models.CharField(max_length=250,null=True)
    pro_price_currency = models.ForeignKey(Currency, null=True,on_delete=models.CASCADE)
    online_pro_qty = models.CharField(max_length=250,null=True,default=0)
    offline_pro_qty = models.CharField(max_length=250,null=True,default=0)
    pro_vat = models.CharField(max_length=250,null=True)
    pro_attr = models.CharField(max_length=200,null=True)
    pro_weight = models.CharField(max_length=200,null=True)
    #pro_image = models.ImageField(upload_to='agent_image',null=True)
    pro_desc = models.TextField(null=True)
    pro_spec = models.TextField(null=True)
    pro_shipping_price = models.CharField(max_length=200,null=True)
    pro_cod = models.BooleanField(default=False)
    pro_exchange_offer = models.CharField(max_length=200,null=True)
    pro_featured = models.BooleanField(default=False)
    pro_status = models.IntegerField(null=True,help_text='0 => Publish,1 => Unpublish')
    pro_publish_by = models.CharField(max_length=200,null=True)
    pro_add_date = models.DateField(null=True)
    pro_edit_date = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pro_brand

    class Meta:
        db_table = 'product_master'

class Productimage(models.Model):
    pro_id = models.CharField(max_length=200,null=True)
    bo_id = models.CharField(max_length=200,null=True)
    pro_image = models.ImageField(upload_to='address_gallery',null=True)
    featured_image = models.BooleanField(default=False)
    image_added_by = models.CharField(max_length=250, null=True)
    image_update_by = models.DateTimeField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pro_id

    class Meta:
        db_table = 'product_image'

class Productattributs_values(models.Model):
    pro_id = models.CharField(max_length=200,null=True)
    attr_id = models.CharField(max_length=200,null=True)
    attr_unit = models.CharField(max_length=200,null=True)
    quantity = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.pro_id

    class Meta:
        db_table = 'product_attribute_values'


class Productquantity_history(models.Model):
    pro_id = models.CharField(max_length=200,null=True)
    online_qty = models.CharField(max_length=200,null=True)
    offline_qty = models.CharField(max_length=200,null=True)
    added_at = models.DateTimeField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pro_id

    class Meta:
        db_table = 'product_quantity_history'


class Productprice_history(models.Model):
    pro_id = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200, null=True)
    added_at = models.DateTimeField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pro_id

    class Meta:
        db_table = 'product_price_history'


class Bo_subscription_mapping(models.Model):
    business_ownerid = models.IntegerField(null=True)
    subscriptionid = models.CharField(max_length=250,null=True)
    subcription_start_date = models.DateTimeField(auto_now_add=True,null=True)
    subcription_end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.business_ownerid

    class Meta:
        db_table = 'bo_subscription_mapping'








