from django.db.models.signals import pre_save
from django.dispatch import receiver

from questionnaires.models import QuestionnaireRow


@receiver(pre_save, sender=QuestionnaireRow)
def create_questionnaire_history(sender, instance, **kwargs):
    if instance.id:
        old_questionnaire = QuestionnaireRow.objects.get(pk=instance.id)
        if old_questionnaire.competence_val != instance.competence_val:
            instance.history.create(competence_val=old_questionnaire.competence_val, date=old_questionnaire.date)
