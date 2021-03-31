from django.shortcuts import render, redirect
from .models import Map, MapPoint, MapPointValue, Conclusion, ExtraInfo
from staff.models import Position
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from dateutil import parser
import json
from datetime import date
from docxtpl import DocxTemplate
import os
from django.conf import settings
from django.db.models import Q
from django.utils.encoding import iri_to_uri
import io

STAGES = {
    1: 'I. Функциональные задачи на срок испытания ',
    2: 'II. Изучение нормативных документов, основных регламентов, положений, стандартов',
    3: 'III. Ознакомление с ИТ-программами, базами данных и т.п., непосредственно касающимися исполнения обязанностей',
    4: 'IV. Оценка професииональных компетенций (при необходимости)',
}

CONCLUSION_TYPES = {
    1: 'ЗАКЛЮЧЕНИЕ НАСТАВНИКА',
    2: 'ЗАКЛЮЧЕНИЕ РУКОВОДИТЕЛЯ',
    3: 'ОСОБОЕ МНЕНИЕ HR - КУРАТОРА',
    4: 'ИТОГОВОЕ ЗАКЛЮЧЕНИЕ',
}


# Create your views here.
def map_list(request):
    maps = Map.objects.select_related('employee').all()
    return render(request, 'map/list.html', {'maps': maps})


def map_detail(request, map_id):
    map_model = Map.objects.prefetch_related('conclusions').get(id=map_id)
    map_points = map_model.map_point_values.select_related('map_point').order_by('map_point__stage_number', 'stage').all()

    grouped_points = dict()
    for point in map_points:
        if point.map_point:
            grouped_points.setdefault(STAGES[point.map_point.stage_number], []).append(point)
        else:
            grouped_points.setdefault(STAGES[point.stage], []).append(point)

    grouped_conclusions = {
        1: {'header': 'ЗАКЛЮЧЕНИЕ НАСТАВНИКА', 'conclusion': None},
        2: {'header': 'ЗАКЛЮЧЕНИЕ РУКОВОДИТЕЛЯ', 'conclusion': None},
        3: {'header': 'ОСОБОЕ МНЕНИЕ HR - КУРАТОРА', 'conclusion': None},
        4: {'header': 'ИТОГОВОЕ ЗАКЛЮЧЕНИЕ', 'conclusion': None},
    }
    for conclusion in map_model.conclusions.all():
        grouped_conclusions[conclusion.type]['conclusion'] = conclusion

    return render(
        request,
        'map/detail.html',
        {
            'map_model': map_model,
            'grouped_points': grouped_points,
            'grouped_conclusions': grouped_conclusions
        }
    )


def get_positions_by_type(request):
    position_type = int(request.GET.get('position_type', 1))
    if position_type == 2:
        result = Position.objects.filter(chief=True).all()
    elif position_type == 3:
        result = Position.objects.filter(chief=False).all()
    else:
        result = Position.objects.all()
    result = serializers.serialize('json', result, fields=('name',))
    return HttpResponse(result, content_type='application/json')


def save_map_point_data(request, point_id):
    if request.is_ajax():
        map_point = MapPointValue.objects.get(pk=point_id)
        data_from_request = json.load(request)
        if data_from_request['point_completing_date']:
            completing_date = parser.parse(data_from_request['point_completing_date'], dayfirst=True).strftime('%Y-%m-%d')
        else:
            completing_date = date.today().strftime('%Y-%m-%d')
        map_point.rating = int(data_from_request['point_rating'])
        map_point.date_of_complete = completing_date
        map_point.save()
        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'Метод запрещен'}, status=403)


def add_map_point(request, map_id, point_type):
    if request.is_ajax():
        data_from_request = json.load(request)
        if data_from_request['map_point_name']:
            map_point = MapPointValue(map_id=map_id, name=data_from_request['map_point_name'], stage=point_type)
            map_point.save()
            return JsonResponse({
                'status': 'OK',
                'map_point': serializers.serialize('json', [map_point])
            })
    return JsonResponse({'status': 'Метод запрещен'}, status=403)


def add_map_conclusion(request, map_id, conclusion_type):
    map_model = Map.objects.get(pk=map_id)
    if request.user.person:
        map_model.conclusions.create(
            type=conclusion_type,
            comment=request.POST.get('comment'),
            final_value=request.POST.get('conclusion_value'),
            author=request.user.person,
            adaptation_map=map_model
        )
    else:
        messages.error(request, 'Пользователю не присвоен сотрудник')
    return redirect(map_model)


def edit_map_conclusion(request, map_id, conclusion_id):
    map_model = Map.objects.get(pk=map_id)
    conclusion = Conclusion.objects.get(pk=conclusion_id)
    conclusion.comment = request.POST.get('comment')
    conclusion.final_value = request.POST.get('conclusion_value')
    conclusion.save(update_fields=['comment', 'final_value'])
    return redirect(map_model)


def export(request, map_id):
    map_model = Map.objects.select_related('employee', 'employee__mentor')\
        .prefetch_related('map_point_values', 'map_point_values__competence', 'map_point_values__map_point', 'map_point_values__map_point__extra_files', 'conclusions')\
        .get(pk=map_id)

    doc = DocxTemplate(os.path.join(settings.BASE_DIR, 'adaptation', 'template_doc', 'adaptation_tpl.docx'))
    chief = map_model.employee.current_department().get_chief()
    mentor = map_model.employee.mentor
    stage_one_items = []
    for item in map_model.map_point_values.filter(Q(map_point__stage_number=1) | Q(stage=1)).all():
        stage_one_items.append({
            'name': item.get_name(),
            'get_completing_date': item.get_completing_date(),
            'complete_status': item.get_rating(),
            'complete_date': item.date_of_complete if item.date_of_complete else '',
            'files': item.get_files()
        })
    stage_two_items = []
    for item in map_model.map_point_values.filter(Q(map_point__stage_number=2) | Q(stage=2)).all():
        stage_two_items.append({
            'name': item.get_name(),
            'files': item.get_files(),
            'complete_status': item.get_rating(),
        })
    stage_three_items = []
    for item in map_model.map_point_values.filter(map_point__stage_number=3).all():
        stage_three_items.append({
            'name': item.get_name(),
            'section': item.map_point.section,
            'files': item.get_files(),
            'complete_status': item.get_rating(),
        })
    competencies = []
    for competence in map_model.map_point_values.select_related('competence').filter(stage=4).all():
        competencies.append({
            'name': competence.competence.name,
            'complete_status': competence.get_rating(),
        })

    # TODO Требуется оптимизация следующих 4-х запросов (возможно ли их уместить в один?)
    try:
        mentor_conclusion = Conclusion.objects.filter(adaptation_map_id=map_model.id, type=1).get()
    except Conclusion.DoesNotExist:
        mentor_conclusion = None
    try:
        department_head_conclusion = Conclusion.objects.filter(adaptation_map_id=map_model.id, type=2).get()
    except Conclusion.DoesNotExist:
        department_head_conclusion = None
    try:
        hr_conclusion = Conclusion.objects.filter(adaptation_map_id=map_model.id, type=3).get()
    except Conclusion.DoesNotExist:
        hr_conclusion = None
    try:
        total_conclusion = Conclusion.objects.filter(adaptation_map_id=map_model.id, type=4).get()
    except Conclusion.DoesNotExist:
        total_conclusion = None

    context = {
        'fio': map_model.employee.fio,
        'position': map_model.employee.current_position().name,
        'department': map_model.employee.current_department().name,
        'department_head': chief.fio,
        'note': map_model.note if map_model.note else '',
        'mentor': mentor.fio,
        'work_start': map_model.employee.current_position_started(),
        'adaptation_stop': map_model.get_map_end_date(),
        'work_type': map_model.employee.get_employment_form(),
        'stage_one_items': stage_one_items,
        'stage_two_items': stage_two_items,
        'stage_three_items': stage_three_items,
        'competencies': competencies,
        'avg_percent': map_model.map_result_percent(),
        'map_result': map_model.map_result_readable_value(),
        'mentor_comments': mentor_conclusion.comment if mentor_conclusion else '',
        'mentor_conclusion_value': mentor_conclusion.get_final_value() if mentor_conclusion else '',
        'department_comments': department_head_conclusion.comment if department_head_conclusion else '',
        'department_conclusion_value': department_head_conclusion.get_final_value() if department_head_conclusion else '',
        'hr_comments': hr_conclusion.comment if hr_conclusion else '',
        'hr_conclusion_value': hr_conclusion.get_final_value() if hr_conclusion else '',
        'total_comments': total_conclusion.comment if total_conclusion else '',
        'total_conclusion_value': total_conclusion.get_final_value() if total_conclusion else '',
    }
    doc.render(context)

    doc_io = io.BytesIO()  # create a file-like object
    doc.save(doc_io)  # save data to file-like object
    doc_io.seek(0)  # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = f"attachment; filename={iri_to_uri('Карта адаптации - ' + map_model.employee.fio)}.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response
