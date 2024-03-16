from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    author_name = forms.CharField(label='Author Name', max_length=255)  # Добавляем новое текстовое поле

    class Meta:
        model = Quote
        fields = ['author_name', 'text', 'tags']  # Включаем новое поле вместо 'author'

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['author_name'].required = False