from django.shortcuts import render, get_object_or_404
from .models import Person
from itertools import groupby
from operator import attrgetter


# Create your views here.
def person_list(request):
    persons = Person.objects.all()
    return render(request, 'staff/person/list.html', {'persons': persons})


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
