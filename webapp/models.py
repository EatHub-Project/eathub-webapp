from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CharField, TextField, DateTimeField, BooleanField
from djangotoolbox.fields import EmbeddedModelField, ListField
from django.core.exceptions import ValidationError
from datetime import datetime


# --- Profile ---

# Validators

def validate_country(self, country):
    if country is None:
        raise ValidationError(u'Country field cannot be empty')
    if self.countries_list.count(country) == 0:
        raise ValidationError(u'%s is not in countries list' % country)


def validate_city(self, city):
    if city is not None:
        if city == '':
            raise ValidationError(u'if city is set it cannot be empty')


def validate_main_language(self, main_language):
    if main_language is None:
        raise ValidationError(u'Main language cannot be empty')
    else:
        if self.languages_list().count(main_language) == 0:
            raise ValidationError(u'%s is not in languages list' % main_language)


def validate_additional_languages(self, additional_languages):
    if additional_languages is not None:
        for a in additional_languages:
            if self.languages_list().count(a) == 0:
                raise ValidationError(u'%s is not in languages list' % additional_languages)


def validate_gender(self, gender):
    #if not (gender.male == 1 or gender.female == 1 or gender.other == 1):
    if not (gender.male == 1 or gender.female == 1):
        raise ValidationError(u'%s is not a valid gender' % gender)


def validate_modification_date(self, modification_date):
    if type(modification_date) is not datetime:  # si no funciona probar con datetime
        raise ValidationError(u'%s is not a date object' % modification_date)


def validate_first_name(self, first_name):
    if first_name is None:
        raise ValidationError(u'the first name cannot be None')


def validate_password(self, password):
    if password.length < 8:
        raise ValidationError(u'the password must be at least 8 characters')


def validate_email(self, email):
    if len(email) > 50 or email is None:
        raise ValidationError(u'Email must be at most 50 characters')


def validate_last_login(self, last_login):
    if type(last_login) is not datetime:
        raise ValidationError(u'last login type must be date')
    if last_login is None:
        raise ValidationError(u'last login cannot be None')
    date = datetime.today()
    if last_login > date:
        raise ValidationError(u'last_login date cannot be after current date')

def validate_gender(self, gender):
    if not (gender == "u" or gender == "m" or gender == "f"):
        raise ValidationError(u'%s is not a valid gender' % gender)


class Location(models.Model):
    country = models.TextField(max_length=50, validators=[validate_country])
    city = models.TextField(max_length=50, null=True, validators=[validate_city])

    def __str__(self):
        return "{}: {}".format(self.country, self.city)


class Tastes(models.Model):
    salty = models.IntegerField()
    sour = models.IntegerField()
    bitter = models.IntegerField()
    sweet = models.IntegerField()
    spicy = models.IntegerField()

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter, self.sweet, self.spicy)


class Profile(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    modification_date = models.DateTimeField(null=True, validators=[validate_modification_date])
    main_language = models.CharField(max_length=50, validators=[validate_main_language])
    additional_languages = ListField(validators=[validate_additional_languages], null=True, blank=False)
    avatar = models.URLField(null=True)
    website = models.URLField(null=True)
    gender = CharField(max_length=1, validators=[validate_gender], null=True)
    birthDate = models.DateField(null=True)
    #embedded
    location = EmbeddedModelField('Location', null=True)
    tastes = EmbeddedModelField('Tastes', null=True)
    user = models.ForeignKey(User, unique=True)

    def __str__(self):
        return str(self.display_name)


# --- Recipe ---

# Validators

def validate_savour(self, savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")


def validate_tags(self, tags):
    if len(tags) > 10:
        raise ValidationError("Max number of tags is 10")


def validate_difficult(self, difficult):
    if difficult <= 0 or difficult >= 4:
        raise ValidationError("Difficult must be in range 1 to 3")


# Models

class Author(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    user_name = models.CharField(max_length=50, blank=False)
    user = ForeignKey(Profile, unique=True)

    def __str__(self):
        return self.displayName

class Picture(models.Model):
    url = models.URLField()
    is_main = models.NullBooleanField()  # BooleanField no acepta valor nulo
    step = IntegerField(null=True)

    def __str__(self):
        return self.url

class Time(models.Model):
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()

    def __str__(self):
        return "{}+{}".format(self.prep_time, self.cook_time)

class Savour(models.Model):
    salty = models.IntegerField(validators=[validate_savour])
    sour = models.IntegerField(validators=[validate_savour])
    bitter = models.IntegerField(validators=[validate_savour])
    sweet = models.IntegerField(validators=[validate_savour])
    spicy = models.IntegerField(validators=[validate_savour])

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter, self.sweet, self.spicy)

class Recipe(models.Model):
    title = CharField(max_length=50, blank=False)
    description = TextField(blank=False)
    creation_date = DateTimeField(auto_now_add=True)
    modification_date = DateTimeField(auto_now_add=True, null=True)
    ingredients = ListField(blank=False)
    serves = CharField(max_length=50, blank=False)
    language = CharField(max_length=50, blank=False)
    temporality = ListField()
    nationality = CharField(max_length=50)
    special_conditions = ListField()
    notes = TextField()
    difficult = IntegerField(validators=[validate_difficult])
    food_type = CharField(max_length=50)
    tags = ListField(validators=[validate_tags])
    steps = ListField(blank=False)

    is_published = BooleanField()
    parent = ForeignKey('self', null=True, blank=True)
    #embedded
    author = EmbeddedModelField('Author')
    pictures = ListField(EmbeddedModelField('Picture'), blank=False)
    time = EmbeddedModelField('Time')
    savours = EmbeddedModelField('Savour')

    def __str__(self):
        return self.title

#enum to entity

class Temporality(models.Model):
    name = CharField(max_length=50, blank=False, unique=True)

class Language(models.Model):
    name = CharField(max_length=50, blank=False, unique=True)

class Food_Type(models.Model):
    name = CharField(max_length=50, blank=False, unique=True)

class Special_Condition(models.Model):
    name = CharField(max_length=50, blank=False, unique=True)
