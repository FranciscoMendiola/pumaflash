# urls.py
from django.urls import path
from django.shortcuts import redirect
from APP.views import AuthView

urlpatterns = [
    path("", lambda request: redirect("auth"), name="root"),
    path("auth/", AuthView.as_view(), name="auth"),
]