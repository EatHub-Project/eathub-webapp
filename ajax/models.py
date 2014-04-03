from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    persist = models.NullBooleanField()