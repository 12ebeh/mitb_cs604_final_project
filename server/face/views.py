from django.shortcuts import render
from django.http import JsonResponse
from .models import UserImage
from .forms import UserImageForm


# Create your views here.
def index(request):
    context = {
        'upload_widget_id_1': 'pic1',
        'upload_widget_id_2': 'pic2'
    }
    return render(request, "face/index.html", context)

def upload_image(request):
    if request.method == 'POST' and request.is_ajax:
        image_id = request.POST.get('imageID')
        uploaded_form = UserImageForm(request.POST, request.FILES)
        if uploaded_form.is_valid():
            img = uploaded_form.save()
            data = {'upload_success': True, 'uploaded_image_id': img.image_id, 'uploaded_image_url': img.image_file.url}
        else:
            data = {'upload_success': False}
        
        return JsonResponse(data)