from django.db import models
# Create your models here.


class Country(models.Model):
    country_name = models.CharField(max_length=500)
    country_code = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'country_master'


class Language(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)
    language_name = models.CharField(max_length=100)
    language_code = models.CharField(max_length=5)
    writing_mode = models.CharField(max_length=10, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.language_name

    class Meta:
        db_table = 'language_master'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True)
    primary_city_id = models.CharField(max_length=5, null=True)
    city_name = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'city_master'


class Verify_user(models.Model):
    verification_code = models.CharField(max_length=250,null=True)
    verify_start_date = models.CharField(max_length=250,null=True)
    verify_end_date = models.CharField(max_length=250,null=True)
    verification_status = models.CharField(max_length=150,null=True)


class Log_conversation(models.Model):
    content_id = models.CharField(max_length=100,null=True)
    content_table = models.CharField(max_length=250,null=True)
    operation = models.CharField(max_length=250,null=True)
    operator_id = models.CharField(max_length=250,null=True)
    log_create_time = models.DateTimeField(auto_now_add=True, null=True)
    operator_type = models.CharField(max_length=200,null=True)
    operation_lang = models.CharField(max_length=200,null=True)

    class Meta:
        db_table = 'log_conversation'
