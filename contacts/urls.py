from django.conf.urls import *

from .views import ContactList, ContactFormView, NewQuoteView, ContactDetail

app_name = "contacts"
urlpatterns = [
  url(r'^new/$', ContactFormView.as_view(), name = "new"),
  url(r'^(?P<contact_id>\d+)/new-quote/$', NewQuoteView.as_view(), name = "new-quote"),
  url(r'^(?P<pk>\d+)/$', ContactDetail.as_view(), name="item"),
  url(r'^$', ContactList.as_view(), name = "index")
]
