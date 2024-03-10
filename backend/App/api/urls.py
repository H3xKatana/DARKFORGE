from django.urls import path
from . import views



urlpatterns=[
    path("login/",views.login_view,name="api_login"),
    path("logout/",views.logout_view,name="api_logout"),
    path("whoami/",views.whoami_view,name="whoami"),
    path("session/",views.session_view,name="session"),
]