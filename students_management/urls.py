from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .settings import base


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.user.urls'))
] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

