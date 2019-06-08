from django import forms

class SearchForm(forms.Form):
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': '검색 단어 입력',
            'class': 'form-control',
            'rows': "3",
            'cols': "500",
            }))
