import re
from datetime import date

from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Loginni kiriting", "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni kiriting", "autocomplete": "current-password"}),
    )
    

class UserForm(forms.ModelForm):
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni kiriting"}),
        min_length=8,
    )
    confirm_password = forms.CharField(
        label="Parolni tasdiqlash",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parolni tasdiqlang"}),
        min_length=8,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "gender",
            "avatar",
            "bio",
            "car",
        ]
        labels = {
            "username": "Username",
            "first_name": "Ism",
            "last_name": "Familiya",
            "email": "Email",
            "phone": "Telefon raqam",
            "birth_date": "Tug'ilgan sana",
            "gender": "Jins",
            "avatar": "Avatar",
            "bio": "Bio",
            "car": "Avtomobil",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismingiz"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Familiyangiz"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@gmail.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "998901234567"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "O'zingiz haqingizda yozing"}),
            "car": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["phone"].required = True
        self.fields["gender"].required = True

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            raise forms.ValidationError("Username faqat harf, raqam va _ dan iborat bo'lishi kerak.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu username allaqachon ro'yxatdan o'tgan.")
        return username

    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name") or "").strip()
        if len(first_name) < 2:
            raise forms.ValidationError("Ism kamida 2 ta belgidan iborat bo'lishi kerak.")
        return first_name

    def clean_last_name(self):
        last_name = (self.cleaned_data.get("last_name") or "").strip()
        if len(last_name) < 2:
            raise forms.ValidationError("Familiya kamida 2 ta belgidan iborat bo'lishi kerak.")
        return last_name

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Email manzili @gmail.com bilan tugashi kerak.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not phone.isdigit():
            raise forms.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak.")
        if len(phone) != 12 and len(phone) != 13:
            raise forms.ValidationError("Telefon raqam to'g'ri formatda bo'lishi kerak.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if not birth_date:
            return birth_date
        if birth_date > date.today():
            raise forms.ValidationError("Tug'ilgan sana kelajak sana bo'lishi mumkin emas.")
        age = (date.today() - birth_date).days // 365
        if age < 16:
            raise forms.ValidationError("Ro'yxatdan o'tish uchun yosh kamida 16 bo'lishi kerak.")
        return birth_date

    def clean_gender(self):
        gender = self.cleaned_data.get("gender")
        valid_choices = {choice[0] for choice in User.GENDER_CHOICES}
        if gender not in valid_choices:
            raise forms.ValidationError("Jinsni to'g'ri tanlang.")
        return gender

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise forms.ValidationError("Parolda kamida bitta harf va bitta raqam bo'lishi kerak.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Parollar mos kelmadi.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "birth_date", "gender", "avatar", "bio", "car"]
        labels = {
            "username": "Username",
            "first_name": "Ism",
            "last_name": "Familiya",
            "email": "Email",
            "phone": "Telefon raqam",
            "birth_date": "Tug'ilgan sana",
            "gender": "Jins",
            "avatar": "Avatar",
            "bio": "Bio",
            "car": "Avtomobil",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "car": forms.Select(attrs={"class": "form-select"}),
        }
