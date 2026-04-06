from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parolni kiriting: '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parolni tasdiqlang: '}))

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        gender = cleaned_data.get("gender")
        username = cleaned_data.get("username")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('confirm_password', "Parollar mos kelmadi.")
        if first_name and last_name:
            raise forms.ValidationError('first_name', "Ism va familiya bo'sh bo'lmasligi kerak.")
        if email not in '@gmail.com':
            raise forms.ValidationError('email', "Email manzili @gmail.com bilan tugashi kerak.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email', "Bu email allaqachon ro'yxatdan o'tgan.")
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError('phone', "Telefon raqam bo'sh bo'lmasligi kerak.")
            if len(phone) != 11:
                raise forms.ValidationError('phone', "Telefon raqam 11 ta raqam bo'lishi kerak.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone', "Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        if User.objects.filter(gender=gender).exists():
            raise forms.ValidationError('gender', "Jinsingizni belgilang.")
        if not username:
            raise forms.ValidationError('username', "Username bo'sh bo'lmasligi kerak.")
        if not username.isalnum():
            raise forms.ValidationError('username', "Username raqam va belgidan iborat bo'lishi kerak.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username', "Bu username allaqachon ro'yxatdan o'tgan.")
        return cleaned_data