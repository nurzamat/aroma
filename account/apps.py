from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        from scheduler import scheduler
        scheduler.start()
