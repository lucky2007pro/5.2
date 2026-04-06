from django import forms

from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "brand",
            "model",
            "year",
            "price",
            "mileage",
            "fuel_type",
            "transmission",
            "engine_volume",
            "color",
            "description",
            "image",
            "is_available",
        ]
        labels = {
            "brand": "Brand",
            "model": "Model",
            "year": "Yil",
            "price": "Narx",
            "mileage": "Yurgan masofa",
            "fuel_type": "Yoqilg'i turi",
            "transmission": "Uzatma",
            "engine_volume": "Dvigatel hajmi",
            "color": "Rang",
            "description": "Tavsif",
            "image": "Rasm",
            "is_available": "Mavjud",
        }
        widgets = {
            "brand": forms.TextInput(attrs={"class": "form-control", "placeholder": "Masalan: Toyota"}),
            "model": forms.TextInput(attrs={"class": "form-control", "placeholder": "Masalan: Camry"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "min": 1886}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.01"}),
            "mileage": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "fuel_type": forms.Select(attrs={"class": "form-select"}),
            "transmission": forms.Select(attrs={"class": "form-select"}),
            "engine_volume": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.1"}),
            "color": forms.TextInput(attrs={"class": "form-control", "placeholder": "Masalan: qora"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Avtomobil haqida qisqacha yozing"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year < 1886 or year > 2026:
            raise forms.ValidationError("Yil 1886 va 2026 orasida bo'lishi kerak.")
        return year

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Narx manfiy bo'lishi mumkin emas.")
        return price

    def clean_mileage(self):
        mileage = self.cleaned_data.get("mileage")
        if mileage < 0:
            raise forms.ValidationError("Yurgan masofa manfiy bo'lishi mumkin emas.")
        return mileage

    def clean_engine_volume(self):
        engine_volume = self.cleaned_data.get("engine_volume")
        if engine_volume < 0:
            raise forms.ValidationError("Dvigatel hajmi manfiy bo'lishi mumkin emas.")
        return engine_volume
