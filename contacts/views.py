from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View

from quotes.models import Quote
from .models import Contact
from .forms import ContactForm


class ContactList(ListView):
    model = Contact
    context_object_name = "contact_list"

class ContactDetail(DetailView):
    model = Contact

class NewQuoteView(View):
    def get(self, request, contact_id, *args, **kwargs):
        quote = Quote.objects.create(contact_id = contact_id)
        return redirect(quote.get_absolute_url)


class ContactFormView(View):
    form_class = ContactForm
    template_name = 'contacts/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts:index')

        return render(request, self.template_name, {'form': form})
