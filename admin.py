from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recruiter

class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('username', 'status')
    list_filter = ('status',)
    actions = ['approve_recruiters', 'reject_recruiters']

    def approve_recruiters(self, request, queryset):
        queryset.update(status='APPROVED')

    def reject_recruiters(self, request, queryset):
        queryset.update(status='REJECTED')

    approve_recruiters.short_description = "Approve selected recruiters"
    reject_recruiters.short_description = "Reject selected recruiters"

admin.site.register(Recruiter, RecruiterAdmin)
