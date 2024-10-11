from tracking.models import Violation
from django.contrib import admin

from django.apps import apps

class DynamicModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = [field.name for field in model._meta.get_fields() if field.concrete]


class ViolationAdmin(DynamicModelAdmin):
    pass

class ViolationTypeAdmin(DynamicModelAdmin):
    pass

# Assuming your app is named 'myapp'
admin.site.register(apps.get_model('tracking', 'Violation'), ViolationAdmin)
admin.site.register(apps.get_model('tracking', 'ViolationType'),  ViolationTypeAdmin)
