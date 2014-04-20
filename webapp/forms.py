import json
from django import forms
from models import Recipe


class NewAccountForm(forms.Form):
    LANGUAGES = [("en", "English"), ("es", "Spanish")]
    GENDERS = [("unknown", "Unspecified"), ("m", "Male"), ("f", "Female")]
    COUNTRY = [("", "--"), ("ES", "Spain"), ("FR", "France"), ("EN", "England"), ("US", "USA")]

    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    display_name = forms.CharField(max_length=50)
    main_language = forms.ChoiceField(choices=LANGUAGES, label="Preferred language")

    additional_languages = forms.MultipleChoiceField(choices=LANGUAGES, required=False)
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


class NewRecipeForm(forms.Form):
    LANGUAGES = [("en", "English"), ("es", "Spanish")]
    COUNTRY = [("", "--"), ("ES", "Spain"), ("FR", "France"), ("EN", "England"), ("US", "USA")]
    TEMPORALITY = [("summer", "Summer"), ("autumn", "Autumn"), ("spring", "Spring"), ("winter", "Winter")]
    FOOD_TYPE = [("dinner","Dinner"),("lunch","Lunch"),("breakfast","Breakfast"),("picnic","Picnic"),("snack","Snack"),("drink","Drink"),("dessert","Dessert")]
    SPECIAL_CONDITIONS = [("diabetic", "Diabetic"), ("celiac", "Celiac"), ("vegetarian", "Vegetarian")]
    DIFFICULT = [(1, "Easy"), (2, "Medium"), (3, "Hard")]

    title = forms.CharField(max_length=50, required=False)
    main_picture_id = forms.CharField(required=True)
    pictures_ids_json = forms.CharField(required=False)
    description = forms.CharField(required=False)

    ingredients_json = forms.CharField(required=True)
    steps_json = forms.CharField(required=True)

    serves = forms.CharField(max_length=50, required=False)
    language = forms.ChoiceField(choices=LANGUAGES, required=False)
    temporality = forms.MultipleChoiceField(choices=TEMPORALITY, required=False)
    nationality = forms.ChoiceField(choices=COUNTRY, required=False)
    special_conditions = forms.MultipleChoiceField(choices=SPECIAL_CONDITIONS, required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    difficult = forms.ChoiceField(choices=DIFFICULT, required=False)
    food_type = forms.ChoiceField(choices=FOOD_TYPE, required=False)
    tags = forms.CharField(required=False)
    prep_time = forms.IntegerField(required=True)
    cook_time = forms.IntegerField(required=True)

    salty = forms.IntegerField(max_value=99, min_value=0, required=False)
    sour = forms.IntegerField(max_value=99, min_value=0, required=False)
    bitter = forms.IntegerField(max_value=99, min_value=0, required=False)
    sweet = forms.IntegerField(max_value=99, min_value=0, required=False)
    spicy = forms.IntegerField(max_value=99, min_value=0, required=False)

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


class EditAccountForm(NewAccountForm):
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['password_repeat'].required = False

class AddComment(forms.Form):
    text = forms.CharField(required=True)
