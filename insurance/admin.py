from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from insurance.models import Customer, Policy, Quote


class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'date_of_birth')}),
    )


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Policy)
admin.site.register(Quote)
