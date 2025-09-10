from django import forms
from .models import Character, CharacterClass


class CharacterForm(forms.ModelForm):
    extra_intelligence = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        label='Дополнительный интеллект'
    )
    extra_dexterity = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        label='Дополнительная ловкость'
    )
    extra_strength = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        label='Дополнительная сила'
    )

    class Meta:
        model = Character
        fields = ['name', 'character_class', 'extra_intelligence',
                  'extra_dexterity', 'extra_strength']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Введите имя персонажа'}),
            'character_class': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        extra_int = cleaned_data.get('extra_intelligence', 0)
        extra_dex = cleaned_data.get('extra_dexterity', 0)
        extra_str = cleaned_data.get('extra_strength', 0)
        if extra_int + extra_dex + extra_str != 5:
            raise forms.ValidationError(
                'Сумма дополнительных очков должна быть ровно 5.')
        return cleaned_data
