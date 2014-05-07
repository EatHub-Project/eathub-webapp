import json
import django
from ajax.models import UploadedImage
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Recipe, Temporality, Food_Type, Language, Special_Condition


class NewAccountForm(forms.Form):
    GENDERS = [("unknown", _("Unspecified")), ("m", _("Male")), ("f", _("Female"))]

    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    display_name = forms.CharField(max_length=50)
    main_language = forms.ChoiceField(label="Preferred language")

    additional_languages = forms.MultipleChoiceField(required=False)
    gender = forms.ChoiceField(choices=GENDERS, required=False)
    location = forms.CharField(max_length=50, required=False)
    website = forms.URLField(required=False)
    birth_date = forms.DateField(required=False)
    avatar_url = forms.URLField(required=False)
    avatar_id = forms.CharField(max_length=200, required=False)

    salty = forms.IntegerField(max_value=99, min_value=0, required=False)
    sour = forms.IntegerField(max_value=99, min_value=0, required=False)
    bitter = forms.IntegerField(max_value=99, min_value=0, required=False)
    sweet = forms.IntegerField(max_value=99, min_value=0, required=False)
    spicy = forms.IntegerField(max_value=99, min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super(NewAccountForm, self).__init__(*args, **kwargs)
        lang=django.utils.translation.get_language().split('-')[0]
        LANGUAGES = Language.get_name_on_language(lang)
        self.fields['main_language'].choices=LANGUAGES
        self.fields['additional_languages'].choices=LANGUAGES


class RecipeForm(forms.Form):
    DIFFICULT = [(1, _("Easy")), (2, _("Medium")), (3, _("Hard"))]

    title = forms.CharField(max_length=50, required=False)
    main_picture_id = forms.CharField(required=True)
    pictures_ids_json = forms.CharField(required=False)
    description = forms.CharField(required=False)

    ingredients_json = forms.CharField(required=True)
    steps_json = forms.CharField(required=True)

    serves = forms.CharField(max_length=50, required=False)
    language = forms.ChoiceField(required=False)
    temporality = forms.MultipleChoiceField(required=False)
    nationality = forms.CharField(max_length=100, required=False)
    special_conditions = forms.MultipleChoiceField(required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    difficult = forms.ChoiceField(choices=DIFFICULT, required=False)
    food_type = forms.ChoiceField(required=False)
    tags = forms.CharField(required=False)
    prep_time = forms.IntegerField(required=True)
    cook_time = forms.IntegerField(required=True)

    salty = forms.IntegerField(max_value=99, min_value=0, required=False)
    sour = forms.IntegerField(max_value=99, min_value=0, required=False)
    bitter = forms.IntegerField(max_value=99, min_value=0, required=False)
    sweet = forms.IntegerField(max_value=99, min_value=0, required=False)
    spicy = forms.IntegerField(max_value=99, min_value=0, required=False)

    def __init__(self):
        lang=django.utils.translation.get_language().split('-')[0]
        LANGUAGES = Language.get_name_on_language(lang)
        TEMPORALITY = Temporality.get_name_on_language(lang)
        FOOD_TYPE = Food_Type.get_name_on_language(lang)
        SPECIAL_CONDITIONS = Special_Condition.get_name_on_language(lang)

        self.language.choices=LANGUAGES
        self.temporality.choices=TEMPORALITY
        self.food_type.choices=FOOD_TYPE
        self.special_conditions.choices=SPECIAL_CONDITIONS

    def get_ingredients_list(self):
        try:
            json_data = self.cleaned_data['ingredients_json']
            data = json.loads(json_data)
            return data
        except AttributeError:
            return None
        except KeyError:
            return None

    def get_pictures_ids_list(self):
        try:
            json_data = self.cleaned_data['pictures_ids_json']
            if json_data:
                data = json.loads(json_data)
                return data
        except AttributeError:
            return None
        except KeyError:
            return None
        return None

    def get_steps_list(self):
        try:
            json_data = self.cleaned_data['steps_json']
            data = json.loads(json_data)
            return data
        except AttributeError:
            return None
        except KeyError:
            return None

    @staticmethod
    def get_filled_form(r):
        data = {
            'title': r.title,
            'description': r.description,
            'main_picture_id': UploadedImage.objects.get(image=r.main_image).id,
            #todo modification?
            'serves': r.serves,
            'language': r.language,
            'temporality': r.temporality,
            'special_conditions': r.special_conditions,
            'nationality': r.nationality,
            'notes': r.notes,
            'difficult': r.difficult,
            'food_type': r.food_type,
            'tags': ",".join(r.tags),
            'cook_time': r.time.cook_time,
            'prep_time': r.time.prep_time,
            'sour': r.savours.sour,
            'sweet': r.savours.sweet,
            'salty': r.savours.salty,
            'bitter': r.savours.bitter,
            'spicy': r.savours.spicy,
        }
        #ingredients
        ingredients_list = r.ingredients
        data['ingredients_json'] = json.dumps(ingredients_list)

        #pictures
        pictures_ids_list = list()
        for pic in r.pictures:
            pictures_ids_list.append(UploadedImage.objects.get(image=pic.image).id)
        data['pictures_ids_json'] = json.dumps(pictures_ids_list)

        #steps
        steps_list = list()
        for step in r.steps:
            if step.image:
                steps_list.append({"text": step.text, "picture": UploadedImage.objects.get(image=step.image).id})
            else:
                steps_list.append({"text": step.text})
        data['steps_json'] = json.dumps(steps_list)

        return RecipeForm(data)


class EditAccountForm(NewAccountForm):
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['password_repeat'].required = False

class SocialAccountForm(NewAccountForm):
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['password_repeat'].required = False

class AddComment(forms.Form):
    text = forms.CharField(required=True)
