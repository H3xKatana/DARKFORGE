from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_cv, name='upload_cv'),
    path('cv_uploaded/', views.cv_uploaded, name='cv_uploaded'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)