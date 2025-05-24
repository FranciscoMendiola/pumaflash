from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View


from APP.forms import CommentForm, ProfileEditForm
from APP.models import Comment, Profile


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, id):
        requested_profile, active_profile = self.__validate_request(
            request, id)
        active_group = requested_profile.id_group
        comments = Comment.objects.filter(id_receiver=requested_profile)

        data = {'requested_profile': requested_profile, 'active_profile': active_profile,
                'active_group': active_group, 'comments': comments}

        return render(request, 'profile.html', data)

    def post(self, request, id):
        requested_profile, active_profile = self.__validate_request(request, id)
        active_group = requested_profile.id_group
        comments = Comment.objects.filter(id_receiver=requested_profile)
        
        data = {'requested_profile': requested_profile, 'active_profile': active_profile,
                'active_group': active_group, 'comments': comments}
        
        tipoFormulario = request.POST.get("tipoFormulario")
        if tipoFormulario == "comment":
            return self.__comment(request, data)
        elif tipoFormulario == "editProfile":
            if request.user == requested_profile.id_user:
                return self.__edit_profile(request, data)
        else:   
            return redirect('profile', id=id)
            
        
    def __comment(self, request, data):
        form = CommentForm(request.POST)
        requested_profile = data['requested_profile'] 
        active_profile = data['active_profile']
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.id_receiver = requested_profile
            comment.id_sender = active_profile
            comment.save()
            # Recargar para mostrar el nuevo comentario
            return redirect('profile', id=requested_profile.id_profile)

        return render(request, 'profile.html', data)
    
    def __edit_profile(self, request, data):
        form = ProfileEditForm(request.user, request.POST, request.FILES)

        active_profile = data['active_profile']

        if form.is_valid():
            # Actualizar datos del usuario
            request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['new_password']:
                request.user.set_password(form.cleaned_data['new_password'])
            if form.cleaned_data['img_url']:
                request.user.img_url = form.cleaned_data['img_url']
            active_profile.description = form.cleaned_data['description']

            active_profile.save()
            # Guardar cambios
            request.user.save()
            update_session_auth_hash(request, request.user)  # Actualizar la sesión del usuario
            messages.success(request, "Perfil actualizado correctamente")
        else:
            self.__get_first_error(request, form)
        
        return render(request, 'profile.html', data)



    def __validate_request(self, request, id):
        # verificamos que el perfil solicitado existe
        requested_profile = get_object_or_404(Profile, id_profile=id)
        active_profile = None

        # Validar permisos
        if request.user.is_staff and requested_profile.id_group.id_admin != request.user:
            raise HttpResponse(
                "El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            active_profile = get_object_or_404(
                Profile, id_group=requested_profile.id_group, id_user=request.user)

        return requested_profile, active_profile
    
    # Función privada para obtener el primer mensaje de error del formulario
    def __get_first_error(self, request, form):
        # Primero buscar errores de campo
        for field_name, field_errors in form.errors.items():
            if field_errors:
                label = form.fields.get(
                    field_name).label if field_name in form.fields else ""
                message = f"{label}: {field_errors[0]}" if label else field_errors[0]
                messages.error(request, message)
                return message
        # Si no hay errores de campo, buscar errores no asociados
        if form.non_field_errors():
            message = form.non_field_errors()[0]
            messages.error(request, message)
            return message
        return None