from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from adaptation.models import Map, MapPoint, MapPointValue
from staff.models import Staff


@receiver(post_save, sender=Staff)
def set_created_attribute(sender, instance, created,  **kwargs):
    if created and instance.person.status == 1:
        # instance_point_type = 2 if instance.person.current_position().chief else 3

        person_map = Map(employee=instance.person)
        person_map.save()

        map_points = MapPoint.objects.filter(positions__name__contains=instance.position.name).all()
        for map_point in map_points:
            map_point_model = MapPointValue(map=person_map, map_point=map_point)
            map_point_model.save()

        categories = instance.person.current_position().competence_category.prefetch_related('competencies').all()
        for category in categories:
            for competence in category.competencies.all():
                map_point_model = MapPointValue(map=person_map, competence=competence, stage=4)
                map_point_model.save()
