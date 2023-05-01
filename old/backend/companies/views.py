from rest_framework import permissions, generics
from backend.companies.models import Company
from backend.companies.serializers import CompanySerializer


class CompanyList(generics.ListAPIView):
    """
    List all companies, or create a new company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a company instance.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
