from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .models import Quiz, Choice


# Create your views here.
def quiz_list(request):
    all_quiz = Quiz.objects.all()
    return render(request, 'quiz/list.html', {'all_quiz': all_quiz})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions', 'questions__choices'), pk=quiz_id)
    return render(request, 'quiz/detail.html', {'quiz': quiz})


def quiz_answer(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions', 'questions__choices'), pk=quiz_id)
    choices = [int(v) for k, v in request.POST.items() if k.startswith('question__')]
    answers = {}
    for choice_id in choices:
        try:
            choice = Choice.objects.get(pk=choice_id)
        except Choice.DoesNotExist:
            choice = None
        if choice:
            answers[choice.question_id] = choice.correct
        else:
            return HttpResponseBadRequest('Неверные параметры запроса.', content_type="text/plain")
    if answers:
        correct_percentage = int(round((list(answers.values()).count(True) / len(quiz.questions.all())) * 100))
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'correct_percentage': correct_percentage})
    else:
        messages.warning(request, 'Не было выбрано ни одного ответа!')
        return render(request, 'quiz/detail.html', {'quiz': quiz})
