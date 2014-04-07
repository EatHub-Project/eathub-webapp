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
    DIFFICULT = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]

    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(required=True)
    ingredients = forms.CharField(required=True)
    serves = forms.CharField(max_length=50, required=True)
    language = forms.ChoiceField(choices=LANGUAGES)
    temporality = forms.MultipleChoiceField(choices=TEMPORALITY)
    nationality = forms.ChoiceField(choices=COUNTRY, required=False)
    special_conditions = forms.MultipleChoiceField(choices=SPECIAL_CONDITIONS)
    notes = forms.CharField(widget=forms.Textarea, required=True)
    difficult = forms.ChoiceField(choices=DIFFICULT, required=False)
    food_type = forms.ChoiceField(choices=FOOD_TYPE, required=False)
    tags = forms.CharField()
    main_image = forms.ImageField(required=True)

    salty = forms.IntegerField(max_value=99, min_value=0, required=False)
    sour = forms.IntegerField(max_value=99, min_value=0, required=False)
    bitter = forms.IntegerField(max_value=99, min_value=0, required=False)
    sweet = forms.IntegerField(max_value=99, min_value=0, required=False)
    spicy = forms.IntegerField(max_value=99, min_value=0, required=False)


class EditAccountForm(NewAccountForm):
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['password_repeat'].required = False

class AddComment(forms.Form):
    text = forms.CharField(required=True)
