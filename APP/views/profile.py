from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from APP.models import Profile


class ProfileView(LoginRequiredMixin, View):
    
    def get(self, request, id):
        requested_profile, active_profile = self.__validate_request(request, id)
        active_group = requested_profile.id_group
        
        data = {'requested_profile': requested_profile, 'active_profile':active_profile,'active_group':active_group}
        
        return render(request, 'profile.html', data)
        
        
    def __validate_request(self, request, id):
        # verificamos que el perfil zolicitado existe
        requested_profile = get_object_or_404(Profile, id_profile=id)
        active_profile = None
        
        # Validar permisos
        if request.user.is_staff and requested_profile.id_group.id_admin != request.user:
            raise HttpResponse("El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            active_profile=get_object_or_404(Profile, id_group=requested_profile.id_group, id_user=request.user)

        return requested_profile,active_profile