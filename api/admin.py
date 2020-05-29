from django.contrib import admin
from . import models


# Register your models here.
class PrecedentCatalogAdmin(admin.ModelAdmin):
    model = models.PrecedentCatalog
    list_display = ('id', 'name')


class PrecedentInline(admin.TabularInline):
    model = models.Precedent


class ParticipantAdmin(admin.ModelAdmin):
    model = models.Participant
    list_display = ('id', 'user', 'name')
    fields = ('user', 'name')
    inlines = [
        PrecedentInline,
    ]


admin.site.register(models.PrecedentCatalog, PrecedentCatalogAdmin)
admin.site.register(models.Participant, ParticipantAdmin)
