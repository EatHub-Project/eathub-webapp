from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import IntegerField, ForeignKey, CharField, TextField, DateTimeField, BooleanField
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from django.core.exceptions import ValidationError
from datetime import datetime
from django_mongodb_engine.contrib import MongoDBManager

# --- Email registration ---

class Activation(models.Model):
    user = models.ForeignKey(User, related_name="activation", unique=True)
    code = models.CharField(max_length=100) #hash del usuario y la fecha
    date = models.DateTimeField()


# --- Profile ---

# Validators

def validate_savour(savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")

def validate_temporality(temporality):
    if temporality is None:
        raise ValidationError("Temporality cannot be none")
    if len(temporality)<1:
        raise ValidationError("Temporality cannot be empty")

def validate_ingredients(ingredients):
    if len(ingredients)==0:
        print "ingredientes de la lista: " + str(ingredients)
        print "longitud de la lista: " + str(len(ingredients))
    if len(ingredients) < 1:
        raise ValidationError("The ingredients cannot be empty")
    for a in ingredients:
        if a is None:
            raise ValidationError("The ingredients cannot be null")

#TODO: decidir que hacemos con la validacion de idiomas, si aqui o si en las vistas
def validate_main_language(main_language):
    pass


def validate_time(time):
    if time is not None:
        if time.cook_time is None and time.prep_time is None:
            raise ValidationError("Cook and preparation time cannot be none as the same time")
        if time.cook_time is not None:
            if time.cook_time <= 0:
                raise ValidationError("Cook time must be higher than 0")
        if time.prep_time is not None:
            if time.prep_time <= 0:
                raise ValidationError("Preparation time must be higher than 0")


def validate_additional_languages(additional_languages):
    if additional_languages is not None:
        print "validar lenguajes adicionales"
    else:
        pass


def validate_steps(steps):
    for a in steps:
        if a is not None:
            if a.text == "" or a.text == " ":
                raise ValidationError("The steps cannot be empty.")
        else:
            raise ValidationError("The steps cannot be none")

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


def validate_past_date(date):
    now = datetime.now()
    if now > date:
        raise ValidationError(u'date cannot be future')


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
    main_language = models.CharField(max_length=50, validators=[])
    additional_languages = ListField(validators=[], null=True, blank=False)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    website = models.URLField(null=True)
    gender = models.CharField(max_length=1, validators=[validate_gender], null=True)
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
    prep_time = models.IntegerField(null=True)
    cook_time = models.IntegerField(null=True)

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
    ingredients = ListField(null=False, blank=False, validators=[validate_ingredients])
    serves = CharField(max_length=50, blank=False)
    language = CharField(max_length=50, blank=False)
    temporality = ListField(null=False, validators=[validate_temporality])
    nationality = CharField(max_length=50, null=True)
    special_conditions = ListField(null=True)
    notes = TextField(null=True)
    difficult = IntegerField(null=True, validators=[validate_difficult])
    food_type = CharField(max_length=50, null=True)
    tags = ListField(null=True, validators=[validate_tags])

    is_published = BooleanField()
    parent = ForeignKey('self', null=True, blank=True)
    #embedded
    steps = ListField(EmbeddedModelField('Step'), null=False, validators=[validate_steps])
    author = ForeignKey(User)
    pictures = ListField(EmbeddedModelField('Picture'), null=True)
    time = EmbeddedModelField('Time', validators=[validate_time])
    savours = EmbeddedModelField('Savour')
    comments = ListField(EmbeddedModelField('Comment'), blank=True)

    positives = ListField(EmbeddedModelField('Vote'))
    negatives = ListField(EmbeddedModelField('Vote'))

    objects = MongoDBManager()

    def __str__(self):
        return self.title

    def get_child_recipes(self):
        return Recipe.objects.filter(parent=self.id)


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
