from django.db import models
#imports from djangotoolbox
from django.db.models import IntegerField, ForeignKey
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField
from django.core.exceptions import ValidationError

#Create your validates here.

def validate_savour(value):
	if value < 0 or value > 99:
		raise ValidationError("%s is not in range 0 to 99" % value)

# Create your models here.

class Author(models.Model):
    displayName = models.TextField()
    userName = models.TextField()
    #user = ForeignKey(Profile, unique=True)

    def __str__(self):
        return self.displayName

class Picture(models.Model):
    url = models.TextField()
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

"""DIFICULT= (
    (1, 'easy'),
    (2, 'nomral'),
    (3, 'hard'),
)"""
		
class Recipe(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    steps = ListField()
    serves = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    creationDate = models.DateTimeField(auto_now_add=True, null=False)
    isPublished = models.BooleanField()
    parent = ForeignKey('self', null=True, unique=True)
    temporality = ListField()
    nationality = models.TextField()
    specialConditions = ListField()
    notes = models.TextField()
    #dificult = models.CharField(max_length=1, choices=DIFICULT)
    foodType = models.TextField()
    tags = ListField()
    #embedded
    author = EmbeddedModelField('Author')
    pictures = ListField(EmbeddedModelField('Picture'))
    time = EmbeddedModelField('Time')
    ingredients = models.TextField()
    savours = EmbeddedModelField('Savour', null=True)
    #changes = ListField(EmbeddedModelField('Change'))

    def __str__(self):
        return self.title
