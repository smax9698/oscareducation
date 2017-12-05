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
    format = forms.ChoiceField(choices = CSV_CHOICES,required=True)


class StatsAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    action_form = UpdateActionForm
    list_display = ('user', 'user_kind', 'when')
    list_filter = ('user_kind',)
    date_hierarchy = 'when'

    def download_csv(self, request, queryset):
        
        response = HttpResponse(content_type='text/csv')
        #get name of page.
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        if request.POST.get('formatt') == '1':
            writer = csv.writer(response, delimiter=";")
        else:
            writer = csv.writer(response)

        writer.writerow(['user', 'user_kind', 'when'])
        for s in queryset:
            writer.writerow([s.user, s.user_kind, s.when])
      

        return response

    download_csv.short_description = "Telecharger en CSV"

    def get_actions(self, request):
        actions = super(StatsAdmin, self).get_actions(request)
        if request.POST.get('formatt'):
            if 'delete_selected' in actions:
                del actions['format']
        return actions

admin.site.register(LoginStats,StatsAdmin)
# Register your models here.
