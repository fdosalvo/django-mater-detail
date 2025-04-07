from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt  # Importante para AJAX POST
from .models import Header, Detail
from .forms import HeaderForm
import csv
from datetime import datetime
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from .forms import HeaderForm


def index(request):
    return render(request, 'index.html')


def header_data(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search = request.GET.get('search[value]', '')
    detail_page = int(request.GET.get('detail_page', 1))  # Página de detalle

    queryset = Header.objects.all()

    if search:
        queryset = queryset.filter(
            Q(description__icontains=search) | Q(message__icontains=search)
        )

    total_records = queryset.count()

    queryset = queryset[start : start + length]

    data = []
    for item in queryset:
        detail_start = (detail_page - 1) * 5  # 5 filas por página de detalle
        detail_end = detail_start + 5
        details = (
            Detail.objects.filter(header=item)
            .values('dni', 'status', 'send_date', 'times')[detail_start:detail_end]
        )
        total_details = Detail.objects.filter(header=item).count()

        data.append(
            {
                'id': item.id,
                'start_date': item.start_date.strftime('%Y-%m-%d'),
                'end_date': item.end_date.strftime('%Y-%m-%d'),
                'description': item.description,
                'quantity': item.quantity,
                'message': item.message,
                'details': list(details),
                'total_details': total_details,  # Total de filas de detalle
            }
        )

    response_data = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data,
    }

    return JsonResponse(response_data)




@csrf_exempt
def header_create(request):
    if request.method == 'POST':
        form = HeaderForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = HeaderForm()
        form_html = render_to_string('header_create_form.html', {'form': form})
        return JsonResponse({'form_html': form_html})