from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.units import mm
from reportlab.lib.colors import white, black, Color
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()

from quotes.models import Quote


def render_to_pdf(response, context_object):
    """
    Create the PDF object, using the response object as its "file."
    """
    width, height = letter

    c = canvas.Canvas(response, pagesize=letter)
    c.setLineWidth(.3)

    _render_logo(c, height)
    _render_address(c, height)
    _render_contact(c, height, context_object.contact)
    if isinstance(context_object, Quote):
        _render_quote_id(c, height, context_object)
        _render_quote_items(c, height, context_object)

    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()


def _render_logo(c, height):
    c.setFillColorRGB(54/255,190/255,138/255)
    c.setStrokeColor(white)
    c.circle(75, height - 90, r = 30, stroke=False, fill = True)

    c.setFont("Helvetica", 43)
    c.setFillColor(white)
    c.drawCentredString(75, height - 107,"S")


def _render_address(c, height):
    """
    :type c: canvas.Canvas
    """
    c.setFillColorRGB(80/255,80/255,80/255)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(45, height - 134, 'Sébastien Briois')

    c.setFont('Helvetica', 9)
    textobject = c.beginText()
    textobject.setTextOrigin(45, height - 146)
    textobject.textLines("""
    27 grand rue
    31460 Loubens Lauragais
    06.84.10.53.00
    sebriois@gmail.com
    SIRET - 
    """)
    c.drawText(textobject)


def _render_quote_id(c, height, quote):
    """
    :type c: canvas.Canvas
    :type quote: quotes.Quote
    """
    c.setFont("Helvetica", 28)
    c.setFillColor(black)
    c.drawRightString(570, height - 80, "DEVIS")

    c.setFont('Helvetica-Bold', 11)
    c.setFillColorRGB(80/255,80/255,80/255)
    c.drawRightString(570, height - 100, quote.quote_id)
    c.setFont('Helvetica', 11)
    c.drawRightString(570, height - 115, "%s/%s/%s" % (quote.creation_date.day, quote.creation_date.month, quote.creation_date.year))


def _render_contact(c, height, contact):
    """
    :type c: canvas.Canvas
    :type contact: contacts.Contact
    """
    c.setFillColorRGB(80/255,80/255,80/255)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(350, height - 134, contact.name)

    c.setFont('Helvetica', 9)
    textobject = c.beginText()
    textobject.setTextOrigin(350, height - 146)
    textobject.textLines([
        contact.address1,
        contact.address2,
        contact.zip_code + " " + contact.city
    ])
    c.drawText(textobject)


def _render_quote_items(c, height, quote):
    data = [['Description', 'PU HT', 'Quantité', 'Total HT', 'TVA']]
    for item in quote.quoteitem_set.all():
        row = [Paragraph(item.description, styles['Normal']), str(item.unit_price), str(item.quantity), str(item.total_price), "0,00%"]
        data.append(row)

    header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color(60/255,61/255,58/255)),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('LINEBELOW', (0, 0), (-1, -1), 0.1, Color(173/255,173/255,173/255)),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (1, 1), (-1, -1), 'TOP'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT')
    ])
    width, height = letter
    t = Table(data, colWidths = (105*mm, 20*mm, 20*mm, 20*mm, 20*mm))
    t.setStyle(header_style)
    t.wrapOn(c, width, height)
    t.drawOn(c, 45, height - 380)