import logging

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from rapidsms.models import Contact, Connection
from rapidsms.messages.outgoing import OutgoingMessage
from rapidsms.router import router
from rapidsms.contrib.ajax.utils import request as ajax_request

from rclickatell.forms import MessageForm


logging.basicConfig(level=logging.DEBUG)


def test(request):
    if request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            post = {
                'contact': form.cleaned_data['contact'].id,
                'message': form.cleaned_data['message'],
                'phone': form.cleaned_data['phone'],
            }
            status, _, _ = ajax_request('rclickatell/test', post=post)
            if status == 200:
                logging.info('Successfully sent message to rclickatell backend')
            else:
                logging.error('Failed to send test Clickatell message')
    else:
        form = MessageForm()
    context = {'form': form}
    return render_to_response('rclickatell/message.html', context,
                              context_instance=RequestContext(request))
