from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Qo'shimcha ma'lumotlar",
            {
                "fields": (
                    "phone",
                    "birth_date",
                    "gender",
                    "avatar",
                    "bio",
                    "updated_at",
                )
            },
        ),
    )
    readonly_fields = ("updated_at",)
