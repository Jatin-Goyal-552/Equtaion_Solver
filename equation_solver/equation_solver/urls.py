from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf.urls.static import static
from equation_solver import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('equation_solver_app.urls'))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)