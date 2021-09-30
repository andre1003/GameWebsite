from django.contrib import admin
from .models import *

admin.site.register(Player)
admin.site.register(Group)
admin.site.register(Match)
#admin.site.register(Decision)

class DecisionAdmin(admin.ModelAdmin):
    list_display = ('DECISION', 'MATCH')
    ordering = ('match',)

    def DECISION(self, obj):
        return str(obj.decision)

    def MATCH(self, obj):
        return str(obj.match)


admin.site.register(Decision, DecisionAdmin)