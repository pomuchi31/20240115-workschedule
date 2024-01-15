from django.contrib import admin
from .models import PersonalinfoModel, SurveyCalendar, ForbiddenPair

from .forms import ForbiddenPairForm

class PersonalinfoModelAdmin(admin.ModelAdmin):
    list_display    = ["id", "user", "item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8"]

class SurveyCalendarAdmin(admin.ModelAdmin):    
    list_display    = ["id", "user", "item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8"]

class ForbiddenPairAdmin(admin.ModelAdmin):
    list_display    = ["id", "users"]


    form = ForbiddenPairForm

    def users(self, obj):
        data     =""
        for u in obj.user.all():
            data += f"{u},"

        return data



admin.site.register(PersonalinfoModel, PersonalinfoModelAdmin)
admin.site.register(SurveyCalendar,SurveyCalendarAdmin)
admin.site.register(ForbiddenPair, ForbiddenPairAdmin)
