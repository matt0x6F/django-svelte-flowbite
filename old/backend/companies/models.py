from django.db import models

from backend.contacts.models import Contact

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    point_of_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name: str = "Company"
        verbose_name_plural: str = "Companies"

    def __str__(self) -> str:
        return self.name
