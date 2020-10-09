from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = Member
    ordering = ('email',"full_name","password","image","cover")
    list_display = ["full_name",'email','image']

    fieldsets = (
        ('Personal info', {'fields': ('full_name','email','password','image','cover')}),
        ("Additional info", {'fields': ('date_joined','is_active','is_superuser','is_staff','user_permissions')}),

        

       )

    readonly_fields =['password','date_joined','last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email', 'password1', 'password2',
            'is_active','is_superuser','is_staff','user_permissions',"cover",
            'image','last_login','date_joined')}
        ),)


admin.site.register(Member,CustomUserAdmin)