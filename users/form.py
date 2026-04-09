import re
from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Login",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Login"}),
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Parol"}),
    )


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "birth_date", "gender", "avatar", "bio"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "998901234567"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if len(username) < 4:
            raise forms.ValidationError("Login kamida 4 ta belgi bo'lishi kerak.")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu login band.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu email oldin ishlatilgan.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip().replace("+", "")
        if not re.fullmatch(r"998\d{9}", phone):
            raise forms.ValidationError("Telefon 998901234567 formatida bo'lsin.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Bu telefon oldin ishlatilgan.")
        return phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if birth_date > date.today():
            raise forms.ValidationError("Tug'ilgan sana kelajak bo'lmaydi.")
        age = (date.today() - birth_date).days // 365
        if age < 16:
            raise forms.ValidationError("Kamida 16 yosh bo'lishi kerak.")
        return birth_date

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Parollar bir xil emas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "birth_date", "gender", "avatar", "bio"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Bu email oldin ishlatilgan.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip().replace("+", "")
        if not re.fullmatch(r"998\d{9}", phone):
            raise forms.ValidationError("Telefon 998901234567 formatida bo'lsin.")
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Bu telefon oldin ishlatilgan.")
        return phone


class UserPasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Joriy parol")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Yangi parol")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Yangi parol (takror)")
