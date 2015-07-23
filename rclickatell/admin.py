from django.contrib import admin

from rclickatell.models import Message, MessageStatus


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'connection', 'api_message_id', 'body')
    ordering = ('-date',)
    list_filter = ('date',)

admin.site.register(Message, MessageAdmin)


class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'recipient', 'ip_address', 'message',
                    'status', 'description')
    ordering = ('-date',)
    list_filter = ('date', 'ip_address', 'status')
    raw_id_fields = ('message',)
    search_fields = ('message__body', 'recipient', 'sender', 'message__pk',
                     'message__api_message_id')

    def description(self, obj):
        return MessageStatus.STATUS_DESC.get(obj.status, '')

admin.site.register(MessageStatus, MessageStatusAdmin)
