from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField

# SOLO FALTARIA ANADIR LAS RESTRICCIONES QUE FALTEN 
# EN EL MODELO 


class Location(models.Model):
    country = models.TextField(max_length=50)
    city = models.TextField(max_length=50, null=True)

    def __str__(self):
        return "Location:<br/>" + "->Country: " + self.country + "<br/>->City: " + self.city


class Tastes(models.Model):
    salty = models.IntegerField()
    sour = models.IntegerField()
    bitter = models.IntegerField()
    sweet = models.IntegerField()
    spicy = models.IntegerField()

    def __str__(self):
        return "Tastes:<br/>->Salty: " + self.salty.__str__() + "<br/>->Sour: " + self.sour.__str__() + \
               "<br/>->Bitter: " + self.bitter.__str__() + "<br/>->Sweet: " + self.sweet.__str__() + \
               "<br/>->Spicy: " + self.spicy.__str__()


class Gender(models.Model):
    male = models.IntegerField(max_length=1)
    female = models.IntegerField(max_length=1)
    other = models.IntegerField(max_length=1)


class Profile(models.Model):
    display_name = models.TextField(max_length=50)
    modification_date = models.DateTimeField(null=True)
    main_language = models.TextField(max_length=50)
    additional_languages = ListField()
    website = models.TextField(max_length=50, null=True)
    # el atributo genero hay que terminar de definirlo: clase aparte, enumerado,...
    gender = EmbeddedModelField('Gender')
    birthDate = models.DateField(null=True)
    location = EmbeddedModelField('Location')
    tastes = EmbeddedModelField('Tastes')

    user = models.ForeignKey(User, unique=True)

    def __str__(self):
        return "Profile:<br/>" + "->Main language: " + self.main_language + "<br/>" + self.location.__str__() + "<br/>" + self.tastes.__str__()
