# urls.py
from django.urls import path
from django.shortcuts import redirect
from APP.views import AuthView, HomeView, ProfileView

urlpatterns = [
    path("", lambda request: redirect("auth"), name="root"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("home/<str:code>", HomeView.as_view(), name="home"),
    path("profile/<str:id>", ProfileView.as_view(), name="profile"),
]