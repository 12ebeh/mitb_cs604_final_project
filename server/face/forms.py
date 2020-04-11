from django import forms
from .models import UserImage

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ('image_id', 'image_file')