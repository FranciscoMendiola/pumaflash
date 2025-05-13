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
        group = self.__verification_request(request, code)

        profiles = Profile.objects.filter(id_group=group)
        students = User.objects.filter(id__in=profiles.values('id_user'))

        data = {
            'user': request.user,
            'group': group,
            'form': StudentSearchForm(),
            'students': students
        }
        return render(request, 'home.html', data)
    
    def post(self, request, code):
        group = self.__verification_request(request, code)

        profiles = Profile.objects.filter(id_group=group)
        students = User.objects.filter(id__in=profiles.values('id_user'))  # Por defecto, todos

        form = StudentSearchForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if username:
                students = students.filter(username__icontains=username)
            if first_name:
                students = students.filter(first_name__icontains=first_name)
            if last_name:
                students = students.filter(last_name__icontains=last_name)
        else:
            form = StudentSearchForm()
                
        data = {
            'user': request.user,
            'group': group,
            'form': form,
            'students': students
        }
        return render(request, 'home.html', data)

    def __verification_request(self, request, code):
        group = get_object_or_404(Group, code=code)

        # Validar permisos
        if request.user.is_staff and group.id_admin != request.user.id:
            raise HttpResponse("El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            get_object_or_404(Profile, id_group=group, id_user=request.user)

        return group
