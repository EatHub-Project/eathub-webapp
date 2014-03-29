from django import forms


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
    country = forms.ChoiceField(choices=COUNTRY, required=False)
    city = forms.CharField(max_length=50, required=False)
    website = forms.URLField(required=False)
    birth_date = forms.DateField(required=False)
    #todo avatar

    salty = forms.IntegerField(max_value=99, min_value=0, required=False)
    sour = forms.IntegerField(max_value=99, min_value=0, required=False)
    bitter = forms.IntegerField(max_value=99, min_value=0, required=False)
    sweet = forms.IntegerField(max_value=99, min_value=0, required=False)
    spicy = forms.IntegerField(max_value=99, min_value=0, required=False)
