from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem
from store.models import Product
from core.models import User

@admin.register(User)   
class UserAdmin(BaseUserAdmin):
    # thie following add_fieldsets attribute is an attribute of
    # the BaseUserAdmin class
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username",
                           "password1", 
                           "password2",
                           "email",
                           "first_name",
                           "last_name"),
            },
        ),
    )
    

class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 1
    autocomplete_fields = ['tag']


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]
    

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)