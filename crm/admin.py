from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render, redirect
from django.contrib import messages
from import_export.admin import ImportExportModelAdmin
from import_export import resources
import csv

from .models import Lead, Client, Note, FollowUp


class LeadResource(resources.ModelResource):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'phone', 'company', 'status',
                  'source', 'assigned_to', 'next_follow_up', 'notes', 'created_at', 'updated_at')
        export_order = fields
        import_id_fields = ['email']


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'company', 'status',
                  'assigned_to', 'next_follow_up', 'notes', 'industry', 'created_at', 'updated_at')
        export_order = fields
        import_id_fields = ['email']


@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin):
    resource_class = LeadResource
    list_display = ('name', 'company', 'status', 'assigned_to',
                    'next_follow_up', 'created_at', 'get_tags')
    list_filter = ('status', 'assigned_to', 'created_at', 'tags')
    search_fields = ('name', 'email', 'company', 'notes')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='lead-import-csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                messages.error(request, "Please select a CSV file.")
                return redirect("..")

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File must be a CSV.")
                return redirect("..")

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Lead.objects.create(
                    name=row.get('name', ''),
                    email=row.get('email', ''),
                    phone=row.get('phone', ''),
                    company=row.get('company', ''),
                    status=row.get('status', 'new'),
                    source=row.get('source', 'other'),
                    notes=row.get('notes', ''),
                    assigned_to=row.get('assigned_to', None),
                    next_follow_up=row.get('next_follow_up', None)
                )

            messages.success(request, "Leads imported successfully!")
            return redirect("..")

        return render(request, "admin/csv_form.html", {"title": "Import Leads"})


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource
    list_display = ('name', 'company', 'status', 'assigned_to',
                    'next_follow_up', 'created_at', 'get_tags')
    list_filter = ('status', 'assigned_to', 'created_at', 'tags')
    search_fields = ('name', 'email', 'company', 'notes')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='client-import-csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                messages.error(request, "Please select a CSV file.")
                return redirect("..")

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File must be a CSV.")
                return redirect("..")

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Client.objects.create(
                    name=row.get('name', ''),
                    email=row.get('email', ''),
                    phone=row.get('phone', ''),
                    company=row.get('company', ''),
                    status=row.get('status', 'new'),
                    assigned_to=row.get('assigned_to', None),
                    next_follow_up=row.get('next_follow_up', None),
                    industry=row.get('industry', 'other'),
                    notes=row.get('notes', '')
                )

            messages.success(request, "Clients imported successfully!")
            return redirect("..")

        return render(request, "admin/csv_form.html", {"title": "Import Clients"})


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'created_by',
                    'created_at', 'get_related_object')
    list_filter = ('created_by', 'created_at')
    search_fields = ('content',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def get_related_object(self, obj):
        if obj.lead:
            url = reverse('admin:crm_lead_change', args=[obj.lead.id])
            return format_html('<a href="{}">{}</a>', url, obj.lead)
        elif obj.client:
            url = reverse('admin:crm_client_change', args=[obj.client.id])
            return format_html('<a href="{}">{}</a>', url, obj.client)
        return '-'
    get_related_object.short_description = 'Related Object'


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('scheduled_date', 'status', 'assigned_to',
                    'get_related_object', 'created_at')
    list_filter = ('status', 'assigned_to', 'scheduled_date')
    search_fields = ('notes',)
    date_hierarchy = 'scheduled_date'
    readonly_fields = ('created_at', 'updated_at')

    def get_related_object(self, obj):
        if obj.lead:
            url = reverse('admin:crm_lead_change', args=[obj.lead.id])
            return format_html('<a href="{}">{}</a>', url, obj.lead)
        elif obj.client:
            url = reverse('admin:crm_client_change', args=[obj.client.id])
            return format_html('<a href="{}">{}</a>', url, obj.client)
        return '-'
    get_related_object.short_description = 'Related Object'
