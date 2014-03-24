from django.db import models
#imports from djangotoolbox
from django.db.models import IntegerField, ForeignKey
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField


# Create your models here.

class Author(models.Model):
    displayName = models.TextField()
    userName = models.TextField()
    #user = ForeignKey(Profile, unique=True)

    def __str__(self):
        return self.displayName

class Ingredient(models.Model):
    quantity=models.IntegerField()
    unit=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
	
    def __str__(self):
	    return str(self.quantity)

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
    salty = models.IntegerField()
    sour = models.IntegerField()
    bitter = models.IntegerField()
    sweet = models.IntegerField()
    spicy = models.IntegerField()

    def __str__(self):
        return str(self.salty) + ", etc..."

"""DIFICULT= (
    (1, 'easy'),
    (2, 'nomral'),
    (3, 'hard'),
)"""
		
class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
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
    ingredients = ListField(EmbeddedModelField('Ingredient'))
    savours = EmbeddedModelField('Savour', null=True)
    #changes = ListField(EmbeddedModelField('Change'))

    def __str__(self):
        return self.title
