import os
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

def generate_upload_path(instance, filename):
    return 'images/{}/raw/{}'.format(instance.session_id, filename)

# Create your models here.
class UserImage(models.Model):
    image_id = models.CharField(max_length=10, blank=False, default='pic1')
    session_id = models.CharField(max_length=128, blank=False, default='42')
    image_file = models.ImageField(upload_to=generate_upload_path)
