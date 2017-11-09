import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    name = models.CharField("Name", max_length = 200)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank = True, null = True)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField("City", max_length=1024)
    country = models.CharField("Country", max_length=1024)

    email = models.EmailField("e-mail")

    class Meta:
        db_table = "contact"

    def get_absolute_url(self):
        return "#"

    def __str__(self):
        return self.name

    def validated_quotes(self):
        return self.quote_set.filter(status = settings.VALIDATED).count()

    def due_invoices_this_year(self):
        this_year = datetime.datetime.today().year
        return self.invoice_set.filter(creation_date__year = this_year, status = settings.DUE).count()

    def paid_invoices_this_year(self):
        this_year = datetime.datetime.today().year
        return self.invoice_set.filter(creation_date__year = this_year, status = settings.PAID).count()
