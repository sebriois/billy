import datetime
from django.db import models
from django.conf import settings
from django.urls import reverse

from contacts.models import Contact


def get_unique_number():
    today = datetime.date.today()
    last_quote = Quote.objects.filter(
        creation_date = today
    ).order_by("id").last()

    if not last_quote:
        digits = "0001"
    else:
        digits = int(last_quote.quote_id[-4:]) + 1
        digits = str(digits).zfill(4)

    return "DEV-%s%s%s%s" % (today.year, today.month, today.day, digits)


class Quote(models.Model):
    quote_id = models.CharField(max_length = 20, default = get_unique_number, editable=False, unique=True)
    contact = models.ForeignKey(Contact)
    status = models.IntegerField(default = settings.DRAFT, choices = settings.STATUS_CHOICES)
    creation_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "quote"

    def get_absolute_url(self):
        return reverse('quotes:item', args=[str(self.id)])

    def total_price(self):
        return sum(item.total_price for item in self.quoteitem_set.all())


class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, verbose_name="Quote")
    description = models.TextField()
    quantity = models.FloatField()
    unit_price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        db_table = "quote_item"
