from django.contrib import admin
from .models import *

admin.site.register(Player)
admin.site.register(Group)
admin.site.register(Match)
admin.site.register(Decision)
admin.site.register(MyOwnTestModel)