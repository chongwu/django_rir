from django.apps import AppConfig


class StaffConfig(AppConfig):
    name = 'staff'
    verbose_name = 'Штат сотрудников'

    def ready(self):
        import staff.signals.handlers
