# urls.py
from django.urls import path
from django.shortcuts import redirect
from APP.views import AuthView, HomeView, ProfileView, AwardsView
from APP.views.codes import GeneratorView, GroupsView

urlpatterns = [
    path("", lambda request: redirect("auth"), name="root"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("home/<str:code>", HomeView.as_view(), name="home"),
    path("generator/", GeneratorView.as_view(), name="generator"),
    path("groups/", GroupsView.as_view(), name="groups"),
    path("profile/<str:id>", ProfileView.as_view(), name="profile"),
    path("awards/<str:code>", AwardsView.as_view(), name="awards"),
]
