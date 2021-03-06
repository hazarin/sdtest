from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppUser


# Register your models here.
class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = AppUser
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "delivery_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)


admin.site.register(AppUser, AppUserAdmin)
