from django.contrib import admin
from django.urls import path, include  # 👈 importante importar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),  # 👈 incluye las urls de tu app
]
