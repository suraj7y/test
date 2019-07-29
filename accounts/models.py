from django.db import models
from common.models import Country, City
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    fynoo_id = models.CharField(max_length=150, null=True)
    company_name = models.CharField(max_length=350, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile_code = models.CharField(max_length=3, default=00, null=True)
    mobile_number = models.CharField(max_length=12, default=12, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=1)
    city = models.ForeignKey(City, on_delete=models.PROTECT, default=1)
    profile_image = models.ImageField(upload_to='agent_image',null=True)
    gender = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=100,null=True)
    education = models.CharField(max_length=450,null=True)
    bank_name = models.CharField(max_length=250, null=True)
    iban_no = models.CharField(max_length=250, null=True)
    maroof_link = models.CharField(max_length=300, null=True)
    services = models.CharField(max_length=300, null=True)
    created_by = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    systemip = models.CharField(max_length=200, null=True)
    system_name = models.CharField(max_length=200, null=True)
    user_type = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(('date joined'), auto_now_add=True)
    role = models.CharField(max_length=50,null=True)
    forgot_password_pin = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_master'


class VerificationCode(models.Model):
    verification_code = models.CharField(max_length=10, null=True)
    user_id = models.CharField(unique=True, null=True, max_length=10)
    start_time = models.CharField(max_length=10, null=True)
    end_time = models.CharField(max_length=10, null=True)
    verification_status = models.CharField(max_length=10, default=0)

    def __str__(self):
        return self.verification_code

    class Meta:
        db_table = 'verification_code_master'
