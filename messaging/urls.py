from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.receive_SMS, name="receive_sms"),
]