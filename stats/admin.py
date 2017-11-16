from django.contrib import admin
from .models import LoginStats
from django.http import HttpResponse


class StatsAdmin(admin.ModelAdmin):
    actions = ['download_csv_2']
    list_display = ('user', 'user_kind', 'when')

    def download_csv(self, request, queryset):
        import csv
        f = open('./some.csv', 'wb')
        writer = csv.writer(f)
        writer.writerow(["user", "user_kind", "when"])
        for s in queryset:
            writer.writerow([s.user, s.user_kind, s.when])

    def download_csv_2(self, request, queryset):
        import csv
        response = HttpResponse(content_type='text/csv')
        #get name of page.
        response['Content-Disposition'] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(["user", "user_kind", "when"])

        for s in queryset:
            writer.writerow([s.user, s.user_kind, s.when])

        return response

    download_csv_2.short_description = "Download CSV file for selected stats."

admin.site.register(LoginStats,StatsAdmin)
# Register your models here.
