from rest_framework import generics, permissions
from backend.contacts.models import Contact
from backend.contacts.serializers import ContactSerializer


class ContactList(generics.ListAPIView):
    """
    List all contacts, or create a new contact.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer()


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a contact instance.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
