# urls.py
from django.urls import path
from django.shortcuts import redirect
from APP.views import AuthView
from APP.views.codes import GeneratorView, GroupsView, PruebaView

urlpatterns = [
    path("", lambda request: redirect("auth"), name="root"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("generator/", GeneratorView.as_view(), name="generator"),
    path("groups/", GroupsView.as_view(), name="groups"),
    path("prueba/<str:code>", PruebaView.as_view(), name="prueba"),
]