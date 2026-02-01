from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(SenderMail)
class SenderMailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'colored_status',
        'created_at',
    )
    search_fields = ('email',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def colored_status(self, obj):
        color = "green" if obj.status else "red"
        text = "Active" if obj.status else "Inactive"
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color, text
        )

    colored_status.short_description = "Status"

@admin.register(RecipientMail)
class RecipientMailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'colored_status', 'created_at')
    search_fields = ('email',)
    list_filter = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def colored_status(self, obj):
        color = 'green' if obj.status == 'active' else 'red'
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.get_status_display()
        )

    colored_status.short_description = "Status"

@admin.register(SubjectLine)
class SubjectLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'colored_status', 'created_at')
    search_fields = ('subject',)
    list_filter = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def colored_status(self, obj):
        color = 'green' if obj.status == 'active' else 'red'
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.get_status_display()
        )

    colored_status.short_description = "Status"

@admin.register(MailBody)
class MailBodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_body', 'colored_status', 'created_at')
    list_filter = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def short_body(self, obj):
        return obj.body[:70] + "..." if len(obj.body) > 70 else obj.body

    short_body.short_description = "Mail Preview"

    def colored_status(self, obj):
        color = 'green' if obj.status == 'active' else 'red'
        return format_html(
            '<b style="color:{};">{}</b>',
            color,
            obj.get_status_display()
        )

    colored_status.short_description = "Status"

@admin.register(WarmupControl)
class WarmupControlAdmin(admin.ModelAdmin):
    list_display = ('time_gap_seconds', 'daily_limit_per_sender', 'is_running')


@admin.register(MailWarmupLog)
class MailWarmupLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'recipient',
        'subject',
        'sent_at',
        'status',
    )
    search_fields = (
        'sender__email',
        'recipient__email',
        'subject__subject',
    )
    list_filter = ('status', 'sent_at')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at',)
