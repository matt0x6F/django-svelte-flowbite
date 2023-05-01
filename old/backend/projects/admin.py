from django.contrib import admin

from .models import Invoice, PaymentDetails, Project, Work

# Register Project model in admin

admin.site.register(Project)
admin.site.register(Work)
admin.site.register(Invoice)
admin.site.register(PaymentDetails)
