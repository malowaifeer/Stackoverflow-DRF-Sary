import os

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stackoverflow.urls', namespace='stackoverflow')),
    path('api/', include('stackoverflow_api.urls', namespace='stackoverflow_api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('docs/', RedirectView.as_view(url=str(os.environ.get('DOCS_URL')))),
]
