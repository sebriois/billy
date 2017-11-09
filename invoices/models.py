from django.db import models
import datetime

# Create your models here.
from contacts.models import Contact
from django.conf import settings

def get_unique_number():
    today = datetime.date.today()
    last_invoice = Invoice.objects.filter(
        creation_date = today
    ).order_by("id").last()

    if not last_invoice:
        digits = "0001"
    else:
        digits = int(last_invoice.invoice_id[-4:]) + 1
        digits = str(digits).zfill(4)

    return "INV-%s%s%s%s" % (today.year, today.month, today.day, digits)


class Invoice(models.Model):
    invoice_id = models.CharField(max_length = 20, default = get_unique_number, editable = False, unique = True)
    contact = models.ForeignKey(Contact)
    status = models.IntegerField(choices = settings.STATUS_CHOICES)
    creation_date = models.DateTimeField("Creation date", auto_now_add=True)
    modification_date = models.DateTimeField("Last modification", auto_now=True)

    class Meta:
        db_table = "invoice"
