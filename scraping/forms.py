from django import forms

from scraping.models import City, Language


class FindForm(forms.Form):
    # забор с формы не айди а слаг значения
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name="slug",
        # required - обязательное
        required=False,
        # вывод поля на страницу
        label='Город',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name="slug",
        required=False,
        label='Специальность',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
