import os
import subprocess
from random import randint
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import UserImage
from .forms import UserImageForm

used_session_id = []


def create_session_id():
    new_rand = randint(0, 65534)
    for new_rand in used_session_id:
        new_rand = randint(0, 65534)
    used_session_id.append(new_rand)
    return new_rand


# Create your views here.
def index(request):
    context = {
        'upload_widget_id_1': 'pic1',
        'upload_widget_id_2': 'pic2',
        'session_id': create_session_id()
    }

    return render(request, "face/index.html", context)


def upload_image(request):
    if request.method == 'POST' and request.is_ajax:
        image_id = request.POST.get('image_id')
        req_session_id = request.POST.get('session_id')
        print("POST image_id for session {}: {}".format(req_session_id, image_id))
        uploaded_form = UserImageForm(request.POST, request.FILES)
        if uploaded_form.is_valid():
            img = uploaded_form.save()
            data = {'upload_success': True, 'uploaded_image_id': img.image_id, 'uploaded_image_url': img.image_file.url}
        else:
            data = {'upload_success': False}
        
        return JsonResponse(data)


def train_images(request):
    if request.method == 'POST' and request.is_ajax:
        req_session_id = request.POST.get('session_id')
        print("Train images in session: {}".format(req_session_id))
        
        # TODO: Call Image extraction script here
        
        data = {
            'train_success': True,
            'session_id': req_session_id,
            'training_status': "Images latent representations extracted"
        }
        
        return JsonResponse(data)
        

def blend_images(request):
    if request.method == 'POST' and request.is_ajax:
        req_session_id = request.POST.get('session_id')
        print("Blend images in session: {}".format(req_session_id))
        
        subprocess.call(['python', os.path.join(settings.STYLEGAN_ROOT, "test_hello.py")])
        
        data = {
            'blend_success': True,
            'session_id': req_session_id
        }
        
        return JsonResponse(data)