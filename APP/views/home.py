from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from APP.models import Group, Profile, User
from APP.forms import StudentSearchForm
from django.db.models import Q

class HomeView(LoginRequiredMixin, View):
    '''
    Vista para mostrar la página principal del grupo al que pertenece el usuario.
    '''
    def get(self, request, code):
        active_group,active_profile = self.__validate_request(request, code)
        
        # Obtener todos los perfiles del grupo activo
        profiles = Profile.objects.filter(id_group=active_group)

        data = {
            'active_group': active_group, # Requerido para navbar
            'active_profile': active_profile, # Requerido por el navbar
            'form': StudentSearchForm(),
            'profiles': profiles,
        }
        return render(request, 'home.html', data)
    
    
    def post(self, request, code):
        active_group, active_profile = self.__validate_request(request, code)

        form = StudentSearchForm(request.POST)

        # Obtener todos los perfiles del grupo activo
        profiles = Profile.objects.filter(id_group=active_group)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Filtrar perfiles
            if username:
                profiles = profiles.filter(id_user__username__icontains=username)
            if first_name:
                profiles = profiles.filter(id_user__first_name__icontains=first_name)
            if last_name:
                profiles = profiles.filter(id_user__last_name__icontains=last_name)
        else:
            form = StudentSearchForm()
            
        data = {
            'active_group': active_group, # Requerido para navbar
            'active_profile': active_profile, # Requerido por el navbar
            'form': form,
            'profiles': profiles,
        }
        return render(request, 'home.html', data)
    

    def __validate_request(self, request, code):
        active_group = get_object_or_404(Group, code=code)
        active_profile = None

        # Validar permisos
        if request.user.is_staff and active_group.id_admin != request.user:
            raise HttpResponse("El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            active_profile = get_object_or_404(Profile, id_group=active_group, id_user=request.user)

        return active_group,active_profile
