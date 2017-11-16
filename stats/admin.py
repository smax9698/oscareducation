from django.contrib import admin
from .models import LoginStats
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib.admin.helpers import ActionForm
from django import forms
import csv

CSV_CHOICES = (
    (1, ("European")),
    (2, ("Standard"))
)


class UpdateActionForm(ActionForm):
    formatt = forms.ChoiceField(choices = CSV_CHOICES,required=True)

class StatsAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    action_form = UpdateActionForm


    list_display = ('user', 'user_kind', 'when')
    def download_csv(self, request, queryset):
        
        response = HttpResponse(content_type='text/csv')
        #get name of page.
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        if request.POST.get('formatt') == '1':
            writer = csv.writer(response, delimiter=";")
        else:
            writer = csv.writer(response)
        
        for s in queryset:
            writer.writerow([s.user, s.user_kind, s.when])
      

        return response

    download_csv.short_description = "Telecharger en CSV"


admin.site.register(LoginStats,StatsAdmin)
# Register your models here.
