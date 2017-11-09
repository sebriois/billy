from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView


from utils.pdf_response import render_to_pdf
from .models import Quote, QuoteItem
from .forms import QuoteForm


class QuoteList(ListView):
    model = Quote
    context_object_name = "quote_list"


class QuoteDetail(DetailView):
    model = Quote
    template_name = "quotes/quote_items.html"


class QuoteAsPDF(DetailView):
    model = Quote

    #
    # def get_context_data(self, **kwargs):
    #     context = super(QuoteAsPDF, self).get_context_data(**kwargs)
    #     context['tasks'] = Task.objects.filter(list=self.object)
    #
    #     return context
    #

    def render_to_response(self, context, **response_kwargs):
        filename = "%s.pdf" % (self.object.quote_id)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="%s"' % filename

        render_to_pdf(response, self.object)

        return response


class QuoteFormView(View):
    form_class = QuoteForm
    template_name = 'quotes/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')

        return render(request, self.template_name, {'form': form})


class QuoteItemCreate(CreateView):
    model = QuoteItem
    fields = ['quote', 'description', 'quantity', 'unit_price']

    def form_valid(self, form):
        form.instance.total_price = round(form.cleaned_data['quantity'] * form.cleaned_data['unit_price'], 2)
        self.success_url = form.cleaned_data['quote'].get_absolute_url()
        return super(QuoteItemCreate, self).form_valid(form)

class QuoteItemDelete(DeleteView):
    model = QuoteItem

    def get_success_url(self, **kwargs):
        return reverse_lazy('quotes:item', kwargs = {"pk": self.object.quote.pk})


def set_status(request, pk):
    quote = get_object_or_404(Quote, id = pk)
    status = request.GET.get("status", 1)
    quote.status = status
    quote.save()
    return redirect(quote.get_absolute_url())