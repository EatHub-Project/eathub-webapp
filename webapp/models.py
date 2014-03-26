from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField
from django.core.exceptions import ValidationError
from datetime import datetime

# SOLO FALTARIA ANADIR LAS RESTRICCIONES QUE FALTEN 
# EN EL MODELO 


def validate_country(self, country):  # Prueba numero 28
    if country is None:
        raise ValidationError(u'Country field cannot be empty')
    if self.countries_list.count(country) == 0:
        raise ValidationError(u'%s is not in countries list' % country)


def validate_city(self, city):  # Prueba numero 29
    if city is not None:
        if city == '':
            raise ValidationError(u'if city is set it cannot be empty')


def validate_main_language(self, main_language):  # Prueba numero 31
    if main_language is None:
        raise ValidationError(u'Main language cannot be empty')
    else:
        if self.languages_list().count(main_language) == 0:
            raise ValidationError(u'%s is not in languages list' % main_language)


def validate_additional_languages(self, additional_languages):  # Prueba numero 32
    if additional_languages is not None:
        for a in additional_languages:
            if self.languages_list().count(a) == 0:
                raise ValidationError(u'%s is not in languages list' % additional_languages)


def validate_gender(self, gender):  # Prueba numero 35
    if not (gender.male == 1 or gender.female == 1 or gender.other == 1):
        raise ValidationError(u'%s is not a valid gender' % gender)


def validate_modification_date(self, modification_date):  # Prueba numero 37
    if type(modification_date) is not datetime:  # si no funciona probar con datetime
        raise ValidationError(u'%s is not a date object' % modification_date)


def validate_first_name(self, first_name):  # Prueba numero 39
    if first_name is None:
        raise ValidationError(u'the first name cannot be None')


def validate_password(self, password): # Prueba numero 40
    if password.length < 8:
        raise ValidationError(u'the password must be at least 8 characters')


def validate_email(self, email): # Prueba numero 41
    if len(email) > 50 or email is None:
        raise ValidationError(u'Email must be at most 50 characters')


def validate_last_login(self, last_login):  # Prueba numero 43
    if type(last_login) is not datetime:
        raise ValidationError(u'last login type must be date')
    if last_login is None:
        raise ValidationError(u'last login cannot be None')
    fecha = datetime.today()
    if last_login > fecha:
        raise ValidationError(u'last_login date cannot be after current date')

class Location(models.Model):
    country = models.TextField(max_length=50, validators=[validate_country])
    city = models.TextField(max_length=50, null=True, validators=[validate_city])

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
    modification_date = models.DateTimeField(null=True, validators=[validate_modification_date])
    main_language = models.TextField(max_length=50, validators=[validate_main_language])
    additional_languages = ListField(validators=[validate_additional_languages])
    website = models.TextField(max_length=50, null=True)
    # el atributo genero hay que terminar de definirlo: clase aparte, enumerado,...
    gender = EmbeddedModelField('Gender', validators=[validate_gender])
    birthDate = models.DateField(null=True)
    location = EmbeddedModelField('Location')
    tastes = EmbeddedModelField('Tastes')

    user = models.ForeignKey(User, unique=True)

    def __str__(self):
        return "Profile:<br/>" + "->Main language: " + self.main_language + "<br/>" + self.location.__str__() + "<br/>" + self.tastes.__str__()