from django.shortcuts import render
from django.db.models import Count, Sum
from questionnaires.models import QuestionnaireRow
from competencies.models import Category, Competence
from itertools import groupby
from django.db.models import F
from operator import attrgetter, itemgetter


# Create your views here.
def corporate_report(request):
    all = QuestionnaireRow.objects.filter(competence_val__gt=0).values('competence__name', 'competence__category__name').annotate(Count('competence'))
    rows = {}
    for row in all.all():
        if row['competence__category__name'] not in rows:
            rows[row['competence__category__name']] = [row]
        else:
            rows[row['competence__category__name']].append(row)
    return render(request, 'reports/corporate.html', {'rows': rows})


def department_report(request):
    return render(request, 'reports/department.html')