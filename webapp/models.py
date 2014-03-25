from django.db import models
#imports from djangotoolbox
from django.db.models import IntegerField, ForeignKey
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django.core.exceptions import ValidationError

#Create your validates here.

def validate_savour(value):
    if value < 0 or value > 99:
        raise ValidationError("Value is not in range 0 to 99")
		
def validate_tags(value):
    if len(value) > 10:
        raise ValidationError("Max number of tags is 10")

def validate_difficult(value):
    if value <= 0 or value >= 4:
        raise ValidationError("Difficult must be in range 1 to 3")
	
# Create your models here.

class Author(models.Model):
    displayName = models.TextField()
    userName = models.TextField()
    #user = ForeignKey(Profile, unique=True)

    def __str__(self):
        return self.displayName

class Picture(models.Model):
    url = models.TextField(null=False, blank=False)
    isMain = models.NullBooleanField()  # BooleanField no acepta valor nulo
    step = IntegerField(null=True)

    def __str__(self):
        return self.url

class Time(models.Model):
    prepTime = models.IntegerField()
    cookTime = models.IntegerField()

    def __str__(self):
        return "{}+{}".format(self.prepTime, self.cookTime)


class Savour(models.Model):
    salty = models.IntegerField(validators=[validate_savour])
    sour = models.IntegerField(validators=[validate_savour])
    bitter = models.IntegerField(validators=[validate_savour])
    sweet = models.IntegerField(validators=[validate_savour])
    spicy = models.IntegerField(validators=[validate_savour])

    def __str__(self):
        return str(self.salty) + ", etc..."
		
class Recipe(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    steps = ListField(null=False, blank=False)
    serves = models.CharField(max_length=50, null=False, blank=False)
    language = models.CharField(max_length=50)
    creationDate = models.DateTimeField(auto_now_add=True, null=False)
    isPublished = models.BooleanField()
    parent = ForeignKey('self', null=True, blank=True)
    temporality = ListField()
    nationality = models.TextField()
    specialConditions = ListField()
    notes = models.TextField()
    difficult = models.IntegerField(validators=[validate_difficult])
    foodType = models.TextField()
    tags = ListField(validators=[validate_tags])
    #embedded
    author = EmbeddedModelField('Author')
    pictures = ListField(EmbeddedModelField('Picture'), null=False)
    time = EmbeddedModelField('Time')
    ingredients = models.TextField(null=False)
    savours = EmbeddedModelField('Savour', null=True)
    #changes = ListField(EmbeddedModelField('Change'))

    def __str__(self):
        return self.title