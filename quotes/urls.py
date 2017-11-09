from django.conf.urls import *

from .views import QuoteList, QuoteDetail, QuoteFormView, QuoteItemCreate, QuoteItemDelete, QuoteAsPDF, set_status

app_name = "quotes"
urlpatterns = [
  url(r'^new/$', QuoteFormView.as_view(), name = "new"),
  url(r'^(?P<pk>\d+)/pdf$', QuoteAsPDF.as_view(), name="pdf"),
  url(r'^(?P<pk>\d+)/set-status$', set_status, name="set-status"),
  url(r'^(?P<pk>\d+)/$', QuoteDetail.as_view(), name="item"),
  url(r'^items/add', QuoteItemCreate.as_view(), name="quote-item-add"),
  url(r'^items/(?P<pk>\d+)/delete', QuoteItemDelete.as_view(), name="quote-item-delete"),
  url(r'^$', QuoteList.as_view(), name = "index")
]
