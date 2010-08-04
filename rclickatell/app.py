from rapidsms.apps.base import AppBase
from rapidsms.models import Connection, Backend
from rapidsms.messages.outgoing import OutgoingMessage

from rclickatell.forms import MessageForm


class ClickatellApp(AppBase):
    def ajax_POST_test(self, get, post):
        form = MessageForm(post)
        if form.is_valid():
            contact = form.cleaned_data['contact']
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']
            backend = Backend.objects.get(name='clickatell')
            connection, _ = Connection.objects.get_or_create(contact=contact,
                                                             identity=phone,
                                                             backend=backend)
            message = OutgoingMessage(connection, message)
            return message.send()
