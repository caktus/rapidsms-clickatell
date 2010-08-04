from django.contrib import admin

from rclickatell.models import Message, MessageStatus


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'connection', 'api_message_id', 'body')
    ordering = ('-date',)
    list_filter = ('date',)

admin.site.register(Message, MessageAdmin)


class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ('message', 'date', 'ip_address', 'sender', 'recipient',
                    'status')
    ordering = ('-date',)
    list_filter = ('date', 'ip_address', 'status')
    raw_id_fields = ('message',)

admin.site.register(MessageStatus, MessageStatusAdmin)
