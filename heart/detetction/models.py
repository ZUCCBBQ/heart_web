from django.db import models

# Create your models here.
from django.utils import timezone


class users(models.Model):
    # user_id = models.CharField('id',max_length=1)
    name = models.CharField('name',primary_key=True,null=False,max_length=15)
    mails = models.EmailField('mails',null=False)
    password = models.CharField('password',null=False,max_length=15)
    reason=models.TextField('reason')
    file_location = models.CharField('file_location',max_length=60)
    create_time = models.DateTimeField('create_time',auto_now_add=True)