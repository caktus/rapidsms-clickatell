from django.conf.urls import url

from rclickatell import views


urlpatterns = [
    url(r'^clickatell/test-message/$', views.test,
        name='clickatell-test-message'),
    url(r'^clickatell/status-callback/$', views.status_callback,
        name='clickatell-callback'),
]
