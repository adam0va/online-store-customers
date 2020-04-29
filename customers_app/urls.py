from django.conf.urls import url
from customers_app import views

urlpatterns = [
    url(r'^customers/$', views.CustomerList.as_view()),
    url(r'^customers/(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.CustomerDetail.as_view()),
]