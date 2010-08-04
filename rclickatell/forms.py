from django import forms

from rapidsms.models import Contact


class MessageForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())
    phone = forms.CharField(help_text='For example: 1223334444')
    message = forms.CharField(widget=forms.Textarea)
