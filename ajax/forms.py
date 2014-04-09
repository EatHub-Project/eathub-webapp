from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class TimeZoneForm(forms.Form):
    timezone = forms.CharField()
