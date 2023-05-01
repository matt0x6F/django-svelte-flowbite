from rest_framework import serializers

from backend.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    List all companies, or create a new company.
    """

    point_of_contact = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="contact-detail"
    )

    class Meta:
        model = Company
        fields: list[str] = [
            "id",
            "name",
            "address",
            "city",
            "state",
            "country",
            "zip_code",
            "phone",
            "email",
            "website",
            "point_of_contact",
        ]
