from django.db import models
from common.models import Country
# Create your models here.


class Currency(models.Model):
    country_name = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)
    currency = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=5)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.currency

    class Meta:
        db_table = 'currency_master'
