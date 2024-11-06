from django.apps import AppConfig
from permit.sync import Permit
from django.conf import settings
class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    permit : Permit= None
    name = 'authentication'
    def ready(self):
        self.permit = Permit(
            pdp=settings.PDP_SERVER,
            token=settings.PERMIT_TOKEN,
        )
        try:
            self.permit.api.resource_instances.create(instance_data={
                "key": settings.APP_KEY,
                "resource": "application",
                "tenant": settings.PERMIT_TENANT
            })
        except:
            print("Application already exists")

