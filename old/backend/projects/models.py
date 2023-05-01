from django.db import models
from backend.contacts.models import Contact

from backend.companies.models import Company


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)
    business_point_of_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="business",
    )
    technical_point_of_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="technical",
    )
    billing_point_of_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="billing",
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


class PaymentDetails(models.Model):
    vendor = models.CharField(max_length=100, choices=[("Venmo", "Venmo")])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateTimeField()
    status = models.CharField(
        max_length=100,
        choices=[("Paid", "Paid"), ("Pending", "Pending"), ("Failed", "Failed")],
    )

    class Meta:
        verbose_name = "Payment Details"
        verbose_name_plural = "Payment Details"

    def __str__(self) -> str:
        return f"{self.vendor} - ${self.amount:.2f}"


class Invoice(models.Model):
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_on = models.DateTimeField(null=True, blank=True)
    delivered_on = models.DateTimeField(null=True, blank=True)
    bill_to_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True
    )
    bill_to_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True
    )
    payment_details = models.ForeignKey(
        PaymentDetails, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        total: float = 0

        for work in Work.objects.filter(invoice=self).all():
            total += work.hours * work.rate

        if self.paid_on is not None:
            return f"{self.description} - ${total:.2f} Paid"

        return f"{self.description} - ${total:.2f} Outstanding"


class Work(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    hours = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    billable = models.BooleanField(default=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Work Logs"

    def __str__(self):
        return f"{self.hours} hours on {self.project.name} @ ${self.rate}/hr"
