"""pumaflash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from APP.views.auth import AuthView

urlpatterns = [
    path('', include('APP.urls')),
    path('admin/', admin.site.urls),
    path('login/', lambda request: redirect("auth"), name="login"),
    path('logout/', LogoutView.as_view(next_page='auth'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "APP.error_views.error_400_view"
handler403 = "APP.error_views.error_403_view"
handler404 = "APP.error_views.error_404_view"
handler500 = "APP.error_views.error_500_view"
