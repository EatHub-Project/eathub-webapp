from django.db import models
import hashlib
import random

def upload_to_name(instance, filename):
    name = hashlib.sha1(str(instance.id) + str(random.random())).hexdigest()
    return 'images/%s.%s' % (name, filename.split('.')[-1])

class UploadedImage(models.Model):
    image = models.ImageField(upload_to=upload_to_name)
    persist = models.NullBooleanField()