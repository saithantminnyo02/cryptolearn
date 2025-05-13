from django import forms

ALGORITHM_CHOICES = [
    ('caesar', 'Caesar Cipher'),
    ('xor', 'XOR Cipher'),
    ('rail', 'Rail Fence Cipher'),
]

class TextEncryptForm(forms.Form):
    algorithm = forms.ChoiceField(
        choices=ALGORITHM_CHOICES,
        widget=forms.Select(attrs={"class": "form-select form-select-sm w-50"})
    )
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "class": "form-control form-control-sm w-50"}))
    key = forms.CharField(
        help_text="Shift (for Caesar), key text (for XOR), or rails (for Rail Fence)",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm w-50"})
    )

class TextEncryptionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "class": "form-control form-control-sm w-50"}))
    key = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-sm w-50"}))

class RailFenceForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "class": "form-control form-control-sm w-50"}))
    rails = forms.IntegerField(
        min_value=2,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm w-50"})
    )

class DESForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm w-50'}))
    key = forms.CharField(
        min_length=8,
        max_length=8,
        error_messages={
            'min_length': 'Key must be exactly 8 characters long.',
            'max_length': 'Key must be exactly 8 characters long.'
        },
        help_text="Enter an 8-character key for DES",
        widget=forms.TextInput(attrs={'maxlength': 8, 'class': 'form-control form-control-sm w-50'})
)

class RSAForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control form-control-sm w-50'}))
    p = forms.IntegerField(label="Prime p", widget=forms.NumberInput(attrs={"class": "form-control form-control-sm w-50"}))
    q = forms.IntegerField(label="Prime q", widget=forms.NumberInput(attrs={"class": "form-control form-control-sm w-50"}))
    e = forms.IntegerField(label="Public exponent e", widget=forms.NumberInput(attrs={"class": "form-control form-control-sm w-50"}))