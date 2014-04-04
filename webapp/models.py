from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CharField, TextField, DateTimeField, BooleanField
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from django.core.exceptions import ValidationError
from datetime import datetime


# --- Profile ---

# Validators

def validate_savour(savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")


#TODO: decidir que hacemos con la validacion de idiomas, si aqui o si en las vistas
def validate_main_language(main_language):
    pass


def validate_additional_languages(additional_languages):
    pass


def validate_last_login(last_login):
    if type(last_login) is not datetime:
        raise ValidationError(u'last login type must be date')
    if last_login is None:
        raise ValidationError(u'last login cannot be None')
    date = datetime.today()
    if last_login > date:
        raise ValidationError(u'last_login date cannot be after current date')


def validate_gender(gender):
    if not (gender == "u" or gender == "m" or gender == "f"):
        raise ValidationError(u'%s is not a valid gender' % gender)


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
    main_language = models.CharField(max_length=50, validators=["""validate_main_language"""])
    additional_languages = ListField(validators=["""validate_additional_languages"""], null=True, blank=False)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    website = models.URLField(null=True)
    gender = models.CharField(max_length=1, validators=[validate_gender], null=True)
    birth_date = models.DateField(null=True)
    location = models.CharField(max_length=50, blank=False)
    tastes = EmbeddedModelField('Tastes', null=True)
    user = models.ForeignKey(User, related_name="profile", unique=True)
    following = ListField(EmbeddedModelField('Following'))

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

class Author(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    user_name = models.CharField(max_length=50, blank=False)
    user = ForeignKey(Profile, unique=True)

    def __str__(self):
        return self.displayName


class Picture(models.Model):
    url = models.URLField(blank=False)
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
    temporality = ListField(null=True)
    nationality = CharField(max_length=50, null=True)
    special_conditions = ListField(null=True)
    notes = TextField(null=True)
    difficult = IntegerField(null=True, validators=[validate_difficult])
    food_type = CharField(max_length=50, null=True)
    tags = ListField(null=True, validators=[validate_tags])
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
