# urls.py
from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("index"), name="redirect"),
    path("pumaflash/", views.index, name="index"),
]