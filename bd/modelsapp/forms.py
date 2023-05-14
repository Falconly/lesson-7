from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Buyer


class ProductSearchNameForm(forms.Form):
    product_name = forms.CharField(label="Поиск по названию", required=False)
    product_name.widget.attrs.update({'class': 'form-control', 'placeholder': 'Поиск'})


class ProductSearchPriceForm(forms.Form):
    product_price = forms.CharField(label="Поиск по цене", required=False)
    product_price.widget.attrs.update(
        {'class': 'form-control', 'placeholder': 'Число должно быть в десятичном виде: 45.34'})


class AddProductForm(forms.ModelForm):
    expiration_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['provider'].empty_label = 'Поставщик не выбран'
        self.fields['expiration_date'].label = 'Дата выхода срока годности'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'width: 100%;'
            })

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            raise ValidationError('Длина превышает 50 символов')

        if any(n.isdigit() for n in name):
            raise ValidationError('В названии не должно быть цифр')

        return name


class AddBuyerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control',
                                                    'style': 'width: 300px;'})

    class Meta:
        model = Buyer
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 50:
            raise ValidationError('Длина превышает 50 символов')

        if any(n.isdigit() for n in name):
            raise ValidationError('Имя не должно содержать цифр')

        return name
