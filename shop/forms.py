from django import forms
from .models import Car
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get("year")
        price = cleaned_data.get("price")
        mileage = cleaned_data.get("mileage")
        if year and (year < 1886 or year > 2024):
            raise forms.ValidationError('year', "Yil 1886 va 2024 orasida bo\'lishi kerak.")
        if price and price < 0:
            raise forms.ValidationError('price', "Narx bo\'lishi kerak.")
        if mileage and mileage < 0:
            raise forms.ValidationError('mileage', "Yurgan masofa manfiy bo\'lmasligi kerak.")
        return cleaned_data