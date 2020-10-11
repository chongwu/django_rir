from django.apps import AppConfig


class QuestionnairesConfig(AppConfig):
    name = 'questionnaires'
    verbose_name = 'Анкеты'

    def ready(self):
        import questionnaires.signals.handlers
