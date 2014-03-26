from django import forms
from models import User


class UserForm(forms.ModelForm):
   class Meta:
      model = User

   def clean_username(self):
      diccionario_limpio = self.cleaned_data
      username = diccionario_limpio.get('username')
      if len(username) <= 3:
         raise forms.ValidationError("Login must have more than three characters")
      return username

   def clean_password(self):
      diccionario_limpio = self.cleaned_data
      password = diccionario_limpio.get('password')
      if len(password) > 20:
         raise forms.ValidationError("Password must be less than 20 characters")
      return password
