from django import forms
from django.core.validators import ValidationError
from bs4 import BeautifulSoup
import requests

class SearchForm(forms.Form):
    id = forms.CharField(max_length=8, label='ID produktu', widget=forms.TextInput(attrs={'placeholder': 'ID produktu np: dla https://www.ceneo.pl/81363724 ID=81363724'}))

    def clean_id(self):
        id = self.cleaned_data['id']
        #Validation if user entered nieprawidlowe id (litery)
        try:
            id = int(id)
        except:
            raise ValidationError("Id produktu muszę skladać się z cyfr, a nie z liter!")

        #True Id must contain 8 numbers
        if len(str(id)) != 8:
            raise ValidationError("Id produktu muszę skladać się z 8 cyfr!")

        #Check if this product exists
        url = f"https://www.ceneo.pl/{id}#tab=reviews"
        page_response = requests.get(url)
        if page_response.status_code != requests.codes.ok:
            raise ValidationError(f'Nie instnieję produktu z id: {id}.')


        return id