from django.apps import AppConfig


class StatsConfig(AppConfig):
    name = 'stats'
    verbose_name = 'Rocket League Stats'

    def ready(self):
        import stats.signals
