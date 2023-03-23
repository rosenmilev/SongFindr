from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter a word'}))
