
from django.contrib import admin
from django.urls import path,include
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.Welcome),
    path("admin/", admin.site.urls),
    path("super-admin/",include("sadmins.urls")),
    path("api/",include("enduser.urls")),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

