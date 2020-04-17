from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('train_images', views.train_images, name='train_images'),
    path('blend_images', views.blend_images, name='blend_images')   
]
