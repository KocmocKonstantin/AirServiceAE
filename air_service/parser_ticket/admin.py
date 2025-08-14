from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'flight_number', 'departure_city', 'arrival_city', 'departure_date', 'departure_time', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'ticket_class', 'uploaded_at')
    search_fields = ('full_name', 'flight_number', 'departure_city', 'arrival_city')
    readonly_fields = ('uploaded_at', 'extracted_text')
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'flight_number', 'departure_city', 'arrival_city', 'departure_date', 'departure_time', 'seat', 'ticket_class')
        }),
        ('Файл', {
            'fields': ('uploaded_file', 'document_type', 'uploaded_at')
        }),
        ('Извлеченный текст', {
            'fields': ('extracted_text',),
            'classes': ('collapse',)
        }),
    )
