from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "is_active",
        ]
        labels = {
            "category": "Kategoriya",
            "name": "Mahsulot nomi",
            "description": "Tavsif",
            "price": "Narx",
            "stock": "Soni",
            "image": "Rasm",
            "is_active": "Faol",
        }
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mahsulot nomi"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Mahsulot haqida to'liq yozing"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": 1000, "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 3:
            raise forms.ValidationError("Mahsulot nomi kamida 3 belgi bo'lishi kerak.")
        return name

    def clean_description(self):
        description = (self.cleaned_data.get("description") or "").strip()
        if len(description) < 20:
            raise forms.ValidationError("Tavsif kamida 20 belgidan iborat bo'lishi kerak.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Narx 0 dan katta bo'lishi kerak.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise forms.ValidationError("Soni manfiy bo'lishi mumkin emas.")
        return stock
