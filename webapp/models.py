from django.db import models
#imports from djangotoolbox
from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField


# Create your models here.

class Author(models.Model):
	displayName = models.TextField()
	#user = ForeignKey(Profile, unique=true)
	
	def __str__(self):
	    return self.displayName

class Picture(models.Model):
    url = models.TextField()
	isMain = models.BooleanField() 
	step = IntegerField()
	
	def __str__(self):
	    return self.url + ", " + self.isMain + ", " + self.step

class Time(models.Model):
    prepTime = models.IntegerField()
	cookTime = models.IntegerField()
	
	def __str__(self):
	    return self.prepTime + ", " + self.cookTime

class Ingredient(models.Model):
    quantity = models.IntegerField()
	unit = models.TextField()
	name = models.TextField()
	
	def __str__(self):
	    return self.name

class Savour(models.Model):
    salty = models.IntegerField()
	sour = models.IntegerField()
	bitter = models.IntegerField()
	sweet = models.IntegerField()
	spicy = models.IntegerField()
	
	def __str__(self):
	    return ""

"""class Change(models.Model):
    attributeName = models.TextField()
	oldValue = #
	newValue = #"""


class Recipe(models.Model):
    title = models.TextField()
	descripcion = models.TextField()
	steps = ListField()
	serves = models.TextField()
	language = models.TextField()
	creationDate = models.DateTimeField(auto_now_add=true, null=false)
	isPublished = models.BooleanField()
	parent = ForeignKey(Recipe, unique=true)
	temporality = ListField()
	nationality = models.TextField()
	specialConditions = ListField()
	notes = models.TextField()
	dificult = models.IntegerField()
	foodType = models.TextField()
	tags = ListField()
	#embedded
	author = EmbeddedModelField('Author')
	pictures = ListField(EmbeddedModelField('Picture'))
	time = EmbeddedModelField('Time')
	ingredients = ListField(EmbeddedModelField('Ingredient'))
	savours = EmbeddedModelField('Savour')
	#changes = ListField(EmbeddedModelField('Change'))
	
	def __str__(self):
	    return self.title
