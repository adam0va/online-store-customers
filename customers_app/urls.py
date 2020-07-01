from django.conf.urls import url
from customers_app import views

urlpatterns = [
    url(r'^all_customers/(?P<user_id>[0-9]+)/$', views.CustomerDetail.as_view()),
    url(r'^all_customers/$', views.AllCustomersList.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^create_new_order/(?P<user_id>[0-9]+)/$', views.NewOrderForCustomer.as_view()),
]