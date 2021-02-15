from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.utils.encoding import smart_str
from .models import Person, Department, Position, Staff
from competencies.models import Category
from questionnaires.models import Questionnaire, QuestionnaireRow, QuestionnaireRowHistory
from itertools import groupby
from operator import attrgetter
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from tempfile import NamedTemporaryFile
from django.contrib import messages
from myrir.utils import group_required
import os


# Create your views here.
def person_list(request, department_id):
    department = Department.objects.get(pk=department_id)
    # persons = Person.objects.all()
    persons = department.workers.filter(person_staff__date_stop__isnull=True)
    return render(request, 'staff/person/list.html', {'department': department, 'persons': persons})


def departments_list(request):
    departments = Department.objects.all()
    return render(request, 'staff/department/list.html', {'departments': departments})


def person_detail(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    questionnaire = person.questionnaires.prefetch_related('rows', 'rows__competence', 'rows__competence__category').first()
    history = QuestionnaireRowHistory.objects.filter(questionnaire_row__questionnaire=questionnaire)\
        .prefetch_related('questionnaire_row__competence').all()
    rows = {}
    if questionnaire:
        rows = {k: list(v) for k, v in groupby(questionnaire.rows.all(), attrgetter('competence.category.name'))}
    return render(request, 'staff/person/detail.html', {'person': person, 'rows': rows, 'history': history})


@group_required('HR')
def create_questionnaire(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    categories = person.position.first().competence_category.all()
    return render(request, 'staff/person/questionnaire_form.html', {'person': person, 'categories': categories})


@group_required('HR')
def upload_questionnaire(request, person_id):
    person = get_object_or_404(Person, tab_number=person_id)
    if request.method == 'POST':
        files = request.FILES['questionnaire']
        if files:
            book = load_workbook(files.file)
            sheet = book.active
            questionnaire = Questionnaire(person=person)
            questionnaire.save()
            rows = []
            for i in range(1, sheet.max_row + 1):
                rows.append(QuestionnaireRow(
                    questionnaire=questionnaire,
                    competence_id=sheet.cell(row=i, column=1).value,
                    competence_val=sheet.cell(row=i, column=3).value if sheet.cell(row=i, column=3).value else 0,
                ))
            QuestionnaireRow.objects.bulk_create(rows)
            messages.success(request, 'Анкета сотрудника успешно загружена!')
    return redirect(person)


@group_required('HR')
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


@group_required('HR')
def upload_department_list(request):
    if request.method == 'POST' and 'departments' in request.FILES:
        files = request.FILES['departments']
        if files:
            book = load_workbook(files.file)
            sheet = book.active
            rows = []
            for i in range(2, sheet.max_row + 1):
                cell_val = sheet.cell(row=i, column=1).value
                if cell_val:
                    rows.append(Department(
                        name=cell_val,
                    ))
            Department.objects.bulk_create(rows)
            messages.success(request, 'Отделы успешно загружены!')
    return redirect('staff:departments_list')


@group_required('HR')
def upload_positions_list(request):
    if request.method == 'POST' and 'positions' in request.FILES:
        files = request.FILES['positions']
        book = load_workbook(files.file)
        sheet = book.active
        for i in range(2, sheet.max_row + 1):
            cell_val = sheet.cell(row=i, column=1).value
            if cell_val:
                new_position = Position.objects.create(
                    name=cell_val
                )
                competence_categories = []
                categories_list = sheet.cell(row=i, column=2).value.split(',')
                for category in categories_list:
                    finded_category = Category.objects.get(name=str.strip(category))
                    if finded_category:
                        competence_categories.append(finded_category)
                new_position.competence_category.add(*competence_categories)
        messages.success(request, 'Список должностей успешно загружен!')
    return redirect('staff:departments_list')


@group_required('HR')
def upload_persons_list(request, department_id):
    if request.method == 'POST' and 'persons' in request.FILES:
        files = request.FILES['persons']
        # @TODO Добавить обработку ошибок, если загружается не xlsx файл
        book = load_workbook(files.file)
        sheet = book.active
        for i in range(2, sheet.max_row + 1):
            cell_val = sheet.cell(row=i, column=1).value
            if cell_val:
                try:
                    exist_person = Person.objects.get(pk=cell_val)
                except Person.DoesNotExist:
                    exist_person = None
                if not exist_person:
                    new_person = Person.objects.create(
                        tab_number=cell_val,
                        fio=sheet.cell(row=i, column=2).value,
                        education=sheet.cell(row=i, column=3).value,
                        experience=sheet.cell(row=i, column=4).value,
                        extra_skill=sheet.cell(row=i, column=5).value,
                    )
                    position = Position.objects.get(name=str.strip(sheet.cell(row=i, column=6).value))
                    if position:
                        start_date = sheet.cell(row=i, column=7).value
                        Staff.objects.create(
                            person=new_person,
                            position=position,
                            department_id=department_id,
                            date_start=start_date.strftime('%Y-%m-%d')
                        )
        messages.success(request, 'Список сотрудников успешно загружен!')
    return redirect('staff:person_list', department_id)
