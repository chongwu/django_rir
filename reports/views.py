from django.shortcuts import render
from django.db.models import Count
from questionnaires.models import QuestionnaireRow
from staff.models import Department
from competencies.models import Competence


# Create your views here.
def report_list(request):
    departments = Department.objects.all()
    return render(request, 'reports/list.html', {'departments': departments})


def corporate_report(request):
    corporate_all = QuestionnaireRow.objects.filter(competence_val__gt=0)\
        .values('competence__name', 'competence__category__name')\
        .annotate(Count('competence'))
    return render(request, 'reports/report.html', {'rows': Competence.prepare_report(corporate_all)})


def department_report(request, department_id):
    department = Department.objects.get(pk=department_id)
    persons = department.workers.filter(person_staff__date_stop__isnull=True).all()
    department_all = QuestionnaireRow.objects.filter(questionnaire__person__tab_number__in=persons)\
        .filter(competence_val__gt=0)\
        .values('competence__name', 'competence__category__name')\
        .annotate(Count('competence'))
    return render(
        request,
        'reports/report.html',
        {'rows': Competence.prepare_report(department_all), 'department': department}
    )
