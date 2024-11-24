from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
        from .models import ProgrammingLanguage
        def add_default_languages(sender, **kwargs):
            default_languages = [
                'Python', 'Java', 'C', 'C++', 'JavaScript', 'Ruby', 'PHP', 
                'Swift', 'Kotlin', 'Go', 'Rust', 'Dart', 'TypeScript', 'Perl',
                'Scala', 'Haskell', 'Lua', 'R', 'MATLAB', 'SQL'
            ]
            for lang in default_languages:
                ProgrammingLanguage.objects.get_or_create(name=lang)
        post_migrate.connect(add_default_languages, sender=self)
