from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt  # Importante para AJAX POST
from .models import Header, Detail
from .forms import HeaderForm
import csv
import datetime
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from .forms import HeaderForm
import io
from django.forms.models import model_to_dict  # Importante para convertir el objeto a dict
import json  # Import para manejar JSON



from django.db.models import Count, Avg

from django.core import serializers

from django.db.models.functions import TruncMonth
from django.db.models import DateField
from django.db.models.functions import Cast
from django.db.models import F

def dashboard_view(request):
    return render(request, 'dashboard.html')

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
            header_instance = form.save()
            # Devolver los datos del objeto creado, importante para confirmar la creación
            return JsonResponse({'success': True, 'data': model_to_dict(header_instance)}, status=200)
        else:
            # Devuelve los errores del formulario en formato JSON
            return JsonResponse({'success': False, 'errors': json.loads(form.errors.as_json())}, status=400)
    else:
        form = HeaderForm()
        form_html = render_to_string('header_create_form.html', {'form': form})
        return JsonResponse({'form_html': form_html})


@csrf_exempt
def detail_upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        header_id = request.POST.get('header_id')  # Obtener header_id desde la petición AJAX

        if not file or not header_id:
            return JsonResponse({'success': False, 'error': 'Archivo o header_id no proporcionado.'})

        try:
            header = Header.objects.get(id=header_id)
        except Header.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Header no encontrado.'})

        try:
            decoded_file = io.TextIOWrapper(file, encoding='utf-8')  # Usar io.TextIOWrapper
            reader = csv.DictReader(decoded_file)

            for row in reader:
                dni = row.get('dni')
                qsend = row.get('qsend')  # Cambiado a qsend
                if dni and qsend:
                    Detail.objects.create(
                        header=header,
                        dni=dni,
                        status=False,  # Valor por defecto
                        send_date=datetime.today().date(),  # Valor por defecto
                        times=int(qsend)  # Guardar qsend en times
                    )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
   
   
   


def dashboard_data(request):
    total_headers = Header.objects.count()
    avg_quantity = Header.objects.aggregate(avg_quantity=Avg('quantity'))['avg_quantity']
    active_headers = Header.objects.filter(end_date__gte=datetime.date.today()).count()

    headers_by_month = Header.objects.annotate(month=TruncMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')

    details_status = Detail.objects.values('status').annotate(count=Count('id'))

    details_avg_times = Detail.objects.annotate(month=TruncMonth('send_date')).values('month').annotate(avg_times=Avg('times')).order_by('month')

    details_by_day = Detail.objects.annotate(send_date_cast=Cast('send_date', output_field=DateField())).values('send_date_cast').annotate(count=Count('id')).order_by('send_date_cast')

    headers_data = serializers.serialize('json', Header.objects.all())

    return JsonResponse({
        'total_headers': total_headers,
        'avg_quantity': avg_quantity,
        'active_headers': active_headers,
        'headers_by_month': list(headers_by_month),
        'details_status': list(details_status),
        'details_avg_times': list(details_avg_times),
        'details_by_day': list(details_by_day),
        'headers_data': json.loads(headers_data),
    })
    