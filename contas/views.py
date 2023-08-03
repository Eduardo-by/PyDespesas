from io import BytesIO

from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView , DeleteView
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from .forms import DespesaForm
from .models import Despesas


class DespesasListView(FormView):
    template_name = "despesas/list.html"
    context_object_name = 'despesas'
    success_url = reverse_lazy('lista_despesas')
    form_class = DespesaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        despesas = Despesas.objects.all()
        total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or 0
        context['despesas'] = despesas
        context['total_despesas'] = total_despesas
        return context


class DespesasDeleteView(DeleteView):
    model = Despesas
    template_name = "despesas/despesa_confirm_delete.html"
    context_object_name = 'despesas'
    success_url = reverse_lazy('lista_despesas')
    def get_success_url(self):
        return self.success_url

def relatorio_despesas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_despesas.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    despesas = Despesas.objects.all()
    total_despesas = despesas.aggregate(total=Sum('valor'))['total'] or 0

    data = [['Data', 'Descrição', 'Valor']]
    for despesa in despesas:
        data.append([despesa.data, despesa.descricao, despesa.valor])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aquamarine),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Despesas", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(table)
    elements.append(
        Paragraph(f"Total das Despesas: R$ {total_despesas:.2f}", styles['Normal']))

    doc.build(elements)

    response.write(buffer.getvalue())
    buffer.close()

    return response
