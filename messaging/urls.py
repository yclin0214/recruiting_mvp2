from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.receive_SMS, name="receive_sms"),
	url(r'^stats$', views.view_statistics, name="view_stats"),
]