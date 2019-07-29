from django.db import models


class Category_Master(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=250)
    category_parent_id = models.IntegerField(null=True)
    category_parent_child_id = models.CharField(max_length=1000, null=True)

    category_user_type = models.CharField(max_length=250, null=True)

    category_created_at = models.DateTimeField(auto_now_add=True, null=True)
    category_created_by = models.IntegerField(null=True)
    category_updated_at = models.DateTimeField(null=True)
    category_updated_by = models.IntegerField(null=True)

    category_status = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category_master'


class Category_Gallery(models.Model):
    category = models.ForeignKey(Category_Master, null=True, on_delete=models.CASCADE)
    category_image = models.ImageField(upload_to='category', blank=True)
    category_featured_img = models.BooleanField(default=False)

    def __str__(self):
        return self.category.category_name + ' Image'

    class Meta:
        db_table = 'category_gallery'


class Filter_Master(models.Model):
    filter_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category_Master, null=True, on_delete=models.PROTECT)

    filter_user_type = models.CharField(max_length=250, null=True)

    filter_created_at = models.DateTimeField(auto_now_add=True, null=True)
    filter_created_by = models.IntegerField(null=True)
    filter_updated_at = models.DateTimeField(null=True)
    filter_updated_by = models.IntegerField(null=True)

    filter_status = models.BooleanField(default=False)

    def __str__(self):
        return self.filter_name

    class Meta:
        db_table = 'filter_master'


class Filter_Value_Master(models.Model):
    filter_value = models.CharField(max_length=100)
    filter = models.ForeignKey(Filter_Master, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.filter_value

    class Meta:
        db_table = 'filter_value_master'

