from django import forms

from users.models import Quote


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Logon',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote_text', 'author_name', 'tags']

    quote_text = forms.CharField(label='Quote', max_length=500)
    author_name = forms.CharField(label='Author', max_length=100)
    tags = forms.CharField(label='Tags', max_length=100)

