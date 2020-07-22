from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url('', include('myapp1.urls')),
    url('admin/', admin.site.urls),
]