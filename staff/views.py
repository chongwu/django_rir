from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.utils.encoding import smart_str
from .models import Person, Department
from questionnaires.models import Questionnaire, QuestionnaireRow
from itertools import groupby
from operator import attrgetter
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from tempfile import NamedTemporaryFile
import os


# Create your views here.
def person_list(request, department_id):
    department = Department.objects.get(pk=department_id)
    # persons = Person.objects.all()
    persons = department.workers.filter(staff__date_stop__isnull=True)
    return render(request, 'staff/person/list.html', {'department': department, 'persons': persons})


def departments_list(request):
    departments = Department.objects.all()
    return render(request, 'staff/department/list.html', {'departments': departments})


def person_detail(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    questionnaire = person.questionnaires.prefetch_related('rows', 'rows__competence', 'rows__competence__category').first()
    rows = {}
    if questionnaire:
        rows = {k: list(v) for k, v in groupby(questionnaire.rows.all(), attrgetter('competence.category.name'))}
    return render(request, 'staff/person/detail.html', {'person': person, 'rows': rows})


def create_questionnaire(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    categories = person.position.first().competence_category.all()
    return render(request, 'staff/person/questionnaire_form.html', {'person': person, 'categories': categories})


def upload_questionnaire(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    if request.method == 'POST':
        files = request.FILES['questionnaire']
        book = load_workbook(files.file)
        sheet = book.active
        questionnaire = Questionnaire(person=person)
        questionnaire.save()
        rows = []
        for i in range(1, sheet.max_row + 1):
            rows.append(QuestionnaireRow(
                questionnaire=questionnaire,
                competence_id=sheet.cell(row=i, column=1).value,
                competence_val=sheet.cell(row=i, column=3).value,
            ))
        QuestionnaireRow.objects.bulk_create(rows)
    return redirect(person)


def download_questionnaire(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    categories = person.position.first().competence_category.all()
    with NamedTemporaryFile(mode='w', delete=False) as f:
        book = Workbook()
        sheet = book.active
        i = 1
        for category in categories:
            for competence in category.competencies.all():
                sheet.cell(row=i, column=1).value = competence.id
                sheet.cell(row=i, column=2).value = competence.name
                i += 1
        book.save(f.name)
        book.close()
        file_name = os.path.basename(f.name)
        response = HttpResponse(content=save_virtual_workbook(book), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name + '.xlsx')
    return response
