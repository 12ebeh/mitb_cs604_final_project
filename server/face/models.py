from django.db import models

# Create your models here.
class UserImage(models.Model):
    image_id = models.CharField(max_length=10, blank=False, default='pic1')
    image_file = models.ImageField(upload_to='images/')