import os
import subprocess
import hashlib
import datetime
from random import randint
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import UserImage
from .forms import UserImageForm

used_session_id = []
session_subprocesses = {}

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

        data = {
            'train_state': 0,
            'session_id': req_session_id
        }

        if (req_session_id not in session_subprocesses):
            print("Start new Train subprocess for session: {}".format(req_session_id))
        
            raw_img_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'raw')
            aligned_img_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'aligned')
            generated_img_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'generated')
            dlatent_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'latent')
            script = os.path.join(settings.STYLEGAN_ROOT,  'run_latent_extraction.py')
            print("Raw Img in Dir: {}".format(raw_img_dir))
            if (os.path.exists(raw_img_dir)):
                print(os.listdir(raw_img_dir))
            print("Script: {}".format(script))

            p = subprocess.Popen(['python', script, raw_img_dir, aligned_img_dir, generated_img_dir, dlatent_dir])
            session_subprocesses[req_session_id] = p
            data['train_stat'] = 1

        return JsonResponse(data)


def poll_training(request):
    if request.method == 'POST' and request.is_ajax:
        req_session_id = request.POST.get('session_id')

        data = {
            'train_state': 0,
            'session_id': req_session_id
        }
        
        if (req_session_id in session_subprocesses):
            ret = session_subprocesses[req_session_id].poll()
            if ret is None:
                data['train_state'] = 1
            elif ret == 0:
                data['train_state'] = 2
                del session_subprocesses[req_session_id]
            else:
                data['train_state'] = -1
                del session_subprocesses[req_session_id]

        return JsonResponse(data)


def blend_images(request):
    if request.method == 'POST' and request.is_ajax:
        req_session_id = request.POST.get('session_id')
        blend = float(request.POST.get('blend'))
        age = float(request.POST.get('age'))
        gender = float(request.POST.get('gender'))
        smile = float(request.POST.get('smile'))
        print("Blend images in session: {}".format(req_session_id))
        print("Blend Factor: {}".format(blend))
        print("Age Factor: {}".format(age))
        print("Gender Factor: {}".format(gender))
        print("Smile Factor: {}".format(smile))

        hash = hashlib.sha1()
        hashstr = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + req_session_id
        hash.update(hashstr.encode('utf-8'))
        salt = hash.hexdigest()[:10]

        results_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'results')
        results_link = os.path.join(settings.MEDIA_URL, 'images', req_session_id, 'results')
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        result_img = os.path.join(results_dir, 'results{}.jpg'.format(salt))
        result_url = os.path.join(results_link, 'results{}.jpg'.format(salt))

        dlatent_dir = os.path.join(settings.MEDIA_ROOT, 'images', req_session_id, 'latent')
        if not os.path.exists(dlatent_dir):
            data = {
                'blend_success': False,
                'session_id': req_session_id
            }
            return JsonResponse(data)
        print("Latent Files:")
        i = 0
        char = []
        for file in os.listdir(dlatent_dir):
            print(file)
            latent = os.path.join(dlatent_dir, file)
            char.append(latent)
            if i >= 2:
                break

        blend_param = "--blend_coeff {}".format(blend)
        age_param = "--age_coeff {}".format(age)
        gender_param = "--gender_coeff {}".format(gender)
        smile_param = "--smile_coeff {}".format(smile)

        script = os.path.join(settings.STYLEGAN_ROOT, 'run_generate_image.py')
        command = ' '.join(['python', script, char[0], char[1], result_img, blend_param, age_param, gender_param, smile_param])
        print(command)
        print(result_url)

        subprocess.run(command, shell=True)

        data = {
            'blend_success': True,
            'session_id': req_session_id,
            'result_url': result_url
        }

        return JsonResponse(data)
        
