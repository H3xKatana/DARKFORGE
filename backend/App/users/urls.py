from django.urls import path
from . import views



from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home_view,
    login_view,
    logout_view,
    forgot_password_view,
    registeration_view,
    check_otp_view,
    check_reset_otp_view,
    reset_new_password_view,
    profile_update_view,
    view_notifications,
)

app_name = 'users'
urlpatterns = [
    path('update/', profile_update_view, name='profile_update'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registeration_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('activate-email/', check_otp_view, name='activate_email'),
    path('reset-code/', check_reset_otp_view, name='reset_code'),
    path('new-password/', reset_new_password_view, name='reset_new_password'),
    path('notifications/', view_notifications, name='view_notifications'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
