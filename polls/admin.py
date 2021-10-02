from django.contrib import admin

from .models import Value, Attribute


class ValueInline(admin.TabularInline):
    model = Value
    extra = 3


class AttributeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['attribute_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('attribute_text', 'pub_date')
    inlines = [ValueInline]

admin.site.register(Attribute, AttributeAdmin)
