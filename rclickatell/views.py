import logging
import pprint

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from rapidsms.contrib.ajax.utils import request as ajax_request

from rclickatell.forms import MessageForm, StatusCallbackForm


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


@csrf_exempt
def status_callback(request):
    form = StatusCallbackForm(request.POST or None)
    if form.is_valid():
        form.save(ip_address=request.get_host())
    else:
        post = pprint.pformat(request.POST)
        errors = [(k, str(v[0])) for k, v in form.errors.items()]
        logging.error('Callback error: %s, %s' % (errors, post))
    return HttpResponse('OK')
