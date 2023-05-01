"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from backend.companies.views import CompanyDetail, CompanyList
from backend.contacts.views import ContactDetail, ContactList
from backend.api.views import get_csrf, login_view, logout_view, SessionView, WhoAmIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/companies/", CompanyList.as_view(), name="company-list"),
    path("api/companies/<int:pk>/", CompanyDetail.as_view(), name="company-detail"),
    path("api/contacts/", ContactList.as_view(), name="contact-list"),
    path("api/contacts/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("api/accounts/csrf/", get_csrf, name="api-csrf"),
    path("api/accounts/login/", login_view, name="api-login"),
    path("api/accounts/logout/", logout_view, name="api-logout"),
    path("api/accounts/session/", SessionView.as_view(), name="api-session"),
    path("api/accounts/whoami/", WhoAmIView.as_view(), name="api-whoami"),
    path("api/accounts/auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
