from django.shortcuts import render, redirect
from staff.models import Person
from questionnaires.models import QuestionnaireRow, Questionnaire, QuestionnaireRowHistory


# Create your views here.
def create_questionnaire(request):
    person_id = request.POST.get('person')
    person = Person.objects.get(tab_number=person_id)
    if request.method == 'POST':
        questionnaire = person.questionnaires.create()
        questionnaire_answers = {k.replace('question__', ''): v for k, v in request.POST.items() if
                                 k.startswith('question__')}
        rows = []
        for competence_id, answer in questionnaire_answers.items():
            rows.append(
                QuestionnaireRow(competence_id=competence_id, questionnaire_id=questionnaire.id, competence_val=answer))
        QuestionnaireRow.objects.bulk_create(rows)

    return redirect(person)


def edit_questionnaire(request, questionnaire_id):
    questionnaire = Questionnaire.objects.prefetch_related('person').get(pk=questionnaire_id)
    person = Person.objects.get(pk=questionnaire.person_id)
    __, rows = person.get_questionnaire_info()
    # TODO Сделать форму Django для создания/редактирования компетенций!!!
    return render(
        request,
        'staff/person/questionnaire_form_edit.html',
        {'person': person, 'rows': rows, 'questionnaire_id': questionnaire.id}
    )


def update_questionnaire(request, questionnaire_id):
    questionnaire = Questionnaire.objects.prefetch_related('rows', 'rows__competence').get(pk=questionnaire_id)
    if request.method == 'POST':
        questionnaire_answers = {k.replace('question__', ''): v for k, v in request.POST.items() if
                                 k.startswith('question__')}
        questionnaire_rows = questionnaire.rows.all()
        rows_history = []
        for row in questionnaire_rows:
            if row.competence_val != (new_val := int(questionnaire_answers[str(row.competence.id)])):
                rows_history.append(QuestionnaireRowHistory(
                    questionnaire_row=row,
                    competence_val=row.competence_val,
                    date=row.date
                ))
                row.competence_val = new_val

        QuestionnaireRow.objects.bulk_update(questionnaire_rows, ['competence_val'])
        QuestionnaireRowHistory.objects.bulk_create(rows_history)
    return redirect(Person.objects.get(pk=questionnaire.person_id))
