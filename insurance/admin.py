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


class PolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_type', 'age_multiplier', 'premium_to_cover_ratio']
    search_fields = ['policy_type']


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['customer', 'policy', 'cover', 'premium', 'status', 'valid_from', 'valid_to']
    search_fields = ['customer', 'policy', 'status']


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Quote, QuoteAdmin)
