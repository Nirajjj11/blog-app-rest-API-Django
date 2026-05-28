from django.contrib import admin
from .models import CustomUser
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
      add_form = CustomUserCreationForm
      form = CustomUserChangeForm
      model = CustomUser
      list_display = [
            'email',
            'username',
            'name',
            'is_staff',
      ]
      
      fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)
      add_fieldsets = (
            (
                  None,
                  {
                        "classes": ("wide",),
                        "fields": (
                        "username",
                        "email",
                        "name",
                        "password1",
                        "password2",
                        ),
                  },
            ),
      )
admin.site.register(CustomUser,CustomUserAdmin)
