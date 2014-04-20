from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CharField, TextField, DateTimeField, BooleanField
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from django.core.exceptions import ValidationError
from datetime import datetime
from django_mongodb_engine.contrib import MongoDBManager


# --- Profile ---

# Validators

def validate_savour(savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")


def validate_last_login(last_login):
    if type(last_login) is not datetime:
        raise ValidationError("last login type must be date")
    if last_login is None:
        raise ValidationError("last login cannot be None")
    date = datetime.today()
    if last_login > date:
        raise ValidationError("last_login date cannot be after current date")


def validate_gender(gender):
    if not (gender == "u" or gender == "m" or gender == "f"):
        raise ValidationError("is not a valid gender")


def validate_past_date(date):
    now = datetime.now()
    if now > date:
        raise ValidationError("date cannot be future")


def validate_additional_language_not_none(additional_languages):
    for language in additional_languages:
        if language is None:
            raise ValidationError("An additional language is not allowed to be none")

def validate_website_is_url(website):
    start = "http://"
    start_sec = "https://"
    if website[:7] != start and website[:8] != start_sec:
        raise ValidationError("Not a valid URL in website")

class Tastes(models.Model):
    salty = models.IntegerField(validators=[validate_savour])
    sour = models.IntegerField(validators=[validate_savour])
    bitter = models.IntegerField(validators=[validate_savour])
    sweet = models.IntegerField(validators=[validate_savour])
    spicy = models.IntegerField(validators=[validate_savour])

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter, self.sweet, self.spicy)


class Profile(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    modification_date = models.DateTimeField(null=True)  #TODO: debe ser pasado, falta meter esta restriccion
    main_language = models.CharField(max_length=50)
    additional_languages = ListField(null=True, blank=False, validators=[validate_additional_language_not_none])
    avatar = models.ImageField(upload_to='avatars/', null=True)
    website = models.URLField(null=True, validators=[validate_website_is_url])
    gender = models.CharField(max_length=1, null=True,validators=[validate_gender])
    birth_date = models.DateField(null=True)
    location = models.CharField(max_length=50, blank=False)
    tastes = EmbeddedModelField('Tastes', null=True)
    user = models.ForeignKey(User, related_name="profile", unique=True)
    following = ListField(EmbeddedModelField('Following'))
    karma = models.IntegerField(default=6)

    objects = MongoDBManager()

    def __str__(self):
        return str(self.display_name)


class Following(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User)

    @staticmethod
    def create_following(user):
        return Following(display_name=user.profile.get().display_name, username=user.username, user=user)

# --- Recipe ---

# Validators

def validate_tags(tags):
    if len(tags) > 10:
        raise ValidationError("Max number of tags is 10")


def validate_difficult(difficult):
    if difficult <= 0 or difficult >= 4:
        raise ValidationError("Difficult must be in range 1 to 3")


# Models

class Comment(models.Model):
    text = models.TextField(blank=False)
    create_date = models.DateTimeField()
    user_own = ForeignKey(User)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.text

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


class Vote(models.Model):
    date = models.DateField(validators=[validate_past_date])
    user = ForeignKey(User)

    def __eq__(self, other):
        return self.user is other.user and self.date == other.date


class Step(models.Model):
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to="images/recipe/",null=True)


class Picture(models.Model):
    image = models.ImageField(upload_to="images/",null=False)


class Recipe(models.Model):
    title = CharField(max_length=50, blank=False)
    description = TextField(blank=False)
    creation_date = DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to="images/recipe/", null=False)
    modification_date = DateTimeField(auto_now_add=True, null=True)
    ingredients = ListField(blank=False)
    serves = CharField(max_length=50, blank=False)
    language = CharField(max_length=50, blank=False)
    temporality = ListField(null=True)
    nationality = CharField(max_length=50, null=True)
    special_conditions = ListField(null=True)
    notes = TextField(null=True)
    difficult = IntegerField(null=True, validators=[validate_difficult])
    food_type = CharField(max_length=50, null=True)
    tags = ListField(null=True, validators=[validate_tags])

    is_published = BooleanField()
    parent = ForeignKey('self', null=True, blank=True)
    #embedded
    steps = ListField(EmbeddedModelField('Step'), null=False)
    author = ForeignKey(User)
    pictures = ListField(EmbeddedModelField('Picture'))
    time = EmbeddedModelField('Time')
    savours = EmbeddedModelField('Savour')
    comments = ListField(EmbeddedModelField('Comment'), blank=True)

    positives = ListField(EmbeddedModelField('Vote'))
    negatives = ListField(EmbeddedModelField('Vote'))

    objects = MongoDBManager()

    def __str__(self):
        return self.title


#enum to entity


class Temporality(models.Model):
    code = CharField(max_length=50, blank=False)
    name_dict = DictField()


class Language(models.Model):
    code = CharField(max_length=50, blank=False)
    name_dict = DictField()


class Food_Type(models.Model):
    code = CharField(max_length=50, blank=False)
    name_dict = DictField()


class Special_Condition(models.Model):
    code = CharField(max_length=50, blank=False)
    name_dict = DictField()
