from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Lead, Client, Note, FollowUp


class LeadResource(resources.ModelResource):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'phone', 'company', 'status',
                  'source', 'assigned_to', 'next_follow_up', 'notes')
        export_order = fields


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'company', 'status',
                  'assigned_to', 'next_follow_up', 'notes')
        export_order = fields


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
