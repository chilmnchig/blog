from django.contrib import admin

from applications.models.monty_hole import MontyHole


class MontyHoleAdmin(admin.ModelAdmin):
    list_display = ('change', 'judge')


admin.site.register(MontyHole, MontyHoleAdmin)
