from django import forms

FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)


class FormatForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))


class DateRangeForm(forms.Form):
    start_date = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'str-date form-control',
            'autocomplete': 'off',
            'placeholder': 'تاریخ شروع'
        }),
        label="تاریخ شروع",
        required=False
    )
    end_date = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'end-date form-control',
            'autocomplete': 'off',
            'placeholder': 'تاریخ پایان'
        }),
        label="تاریخ پایان",
        required=False
    )
