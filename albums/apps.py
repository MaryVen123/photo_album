from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AlbumsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'albums'

    def ready(self):
        from django.contrib.auth.models import User
        
        def create_default_superuser(sender, **kwargs):
            try:
                if not User.objects.filter(username='admin').exists():
                    User.objects.create_superuser('admin', 'admin@example.com', 'Admin@12345')
                    print('✅ Default superuser created: admin / Admin@12345')
            except Exception as e:
                print(f'Superuser creation skipped: {e}')
        
        post_migrate.connect(create_default_superuser)
