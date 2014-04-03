from ajax.forms import ImageUploadForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from ajax.models import UploadedImage
import json


def test(request):
    form = ImageUploadForm()
    return render(request, 'ajax/upload_image.html', {"form": form})


def upload_picture(request):
    f = request.FILES['image']
    img = UploadedImage(image=f)
    img.save()
    return HttpResponse(json.dumps({"id": img.id, "url": img.image.url}))