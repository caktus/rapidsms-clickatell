import time
import datetime

from django import forms

from rapidsms.models import Contact

from rclickatell.models import Message, MessageStatus


class MessageForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())
    phone = forms.CharField(help_text='For example: 1223334444')
    message = forms.CharField(widget=forms.Textarea)


class StatusCallbackForm(forms.Form):
    cliMsgId = forms.ModelChoiceField(queryset=Message.objects.all())
    api_id = forms.IntegerField(min_value=0)
    apiMsgId = forms.CharField()
    timestamp = forms.IntegerField(min_value=0)
    to = forms.IntegerField(min_value=0)
    from_ = forms.CharField(required=False)
    charge = forms.CharField()
    status = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(StatusCallbackForm, self).__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_']
        self.fields.pop('from_')

    def clean_timestamp(self):
        ts = time.mktime(time.localtime(self.cleaned_data['timestamp']))
        return datetime.datetime.fromtimestamp(ts)

    def save(self, ip_address):
        return MessageStatus.objects.create(
            message=self.cleaned_data['cliMsgId'],
            ip_address=ip_address,
            date=self.cleaned_data['timestamp'],
            sender=self.cleaned_data['from'],
            recipient=self.cleaned_data['to'],
            status=self.cleaned_data['status'],
            api_id=self.cleaned_data['api_id'],
            charge=self.cleaned_data['charge'],
        )
