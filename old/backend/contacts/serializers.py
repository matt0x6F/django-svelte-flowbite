from rest_framework import serializers

from backend.contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    List all companies, or create a new company.
    """

    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
