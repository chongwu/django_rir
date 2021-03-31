from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import DevelopmentPlan
from django.conf import settings
from django.utils.encoding import iri_to_uri
from docxtpl import DocxTemplate
import json
import os
import io


ACTIVITY_STATUSES = {
    2: 'Выполненные',
    1: 'Запланированные',
    0: 'Не выполненные',
}


# Create your views here.
def plan_detail(request, plan_id):
    plan = get_object_or_404(DevelopmentPlan.objects.prefetch_related('activities', 'plan_activities').order_by('-activities__activity_status'), pk=plan_id)
    activities = dict()
    for activity in plan.activities.all():
        activities.setdefault(ACTIVITY_STATUSES[activity.activity_status], []).append(activity)
    activities_totals = {activity_type:len(activities) for activity_type, activities in activities.items()}
    return render(
        request,
        'development_plan/detail.html',
        {
            'plan': plan,
            'activities': activities,
            'labels': json.dumps(list(activities_totals.keys())),
            'data': json.dumps(list(activities_totals.values())),
        }
    )


def plan_export(request, plan_id):
    plan = DevelopmentPlan.objects.prefetch_related(
        'activities',
        'plan_activities',
        'employee',
        'employee__department'
    ).get(pk=plan_id)
    doc = DocxTemplate(os.path.join(settings.BASE_DIR, 'development_plan', 'template_doc', 'dev_plan_tpl.docx'))

    # TODO Вынести в метод модели DevelopmentPlan
    activities = dict()
    for activity in plan.activities.all():
        activities.setdefault(ACTIVITY_STATUSES[activity.activity_status], []).append(activity)

    context = {
        'fio': plan.employee.fio,
        'position': plan.employee.current_position().name,
        'header':  plan.employee.current_department().get_chief().fio,
        'complete_activities': [{
            'act_values': activity.values if activity.values else '',
            'activity_type': activity.get_type(),
            'name': activity.name,
            'hours': activity.hours,
            'start': activity.start.strftime('%d.%m.%Y') if activity.start else '',
            'stop': activity.stop.strftime('%d.%m.%Y') if activity.stop else ''
        } for activity in activities['Выполненные']],
        'plan_activities': [{
            'act_values': activity.values if activity.values else '',
            'activity_type': activity.get_type(),
            'name': activity.name,
            'hours': activity.hours,
            'required_up_to': activity.required_up_to if activity.required_up_to else '',
            'status': activity.get_status() if activity.status else ''
        } for activity in activities['Запланированные']],
        'uncomplete_activities': [{
            'act_values': activity.values if activity.values else '',
            'activity_type': activity.get_type(),
            'name': activity.name,
            'hours': activity.hours,
            'required_up_to': activity.required_up_to if activity.required_up_to else '',
            'note': activity.note if activity.note else ''
        } for activity in activities['Не выполненные']],
        'plan_progress': '',
        'ext_activities': [{
            'act_values': activity.values if activity.values else '',
            'method': activity.method,
            'required_up_to': activity.required_up_to,
            'plan': activity.plan,
        } for activity in plan.plan_activities.all()],
    }
    doc.render(context)

    doc_io = io.BytesIO()  # create a file-like object
    doc.save(doc_io)  # save data to file-like object
    doc_io.seek(0)  # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response[
        "Content-Disposition"] = f"attachment; filename={iri_to_uri('Индивидуальный план развития - ' + plan.employee.fio)}.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return response
