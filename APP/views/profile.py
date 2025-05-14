from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View


from APP.forms import CommentForm
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

        requested_profile, active_profile = self.__validate_request(
            request, id)
        active_group = requested_profile.id_group

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.id_receiver = requested_profile
            comment.id_sender = get_object_or_404(
                Profile, id_user=request.user)
            comment.save()
            # Recargar para mostrar el nuevo comentario
            return redirect('profile', id=id)

        comments = Comment.objects.filter(id_receiver=requested_profile)
        data = {'requested_profile': requested_profile, 'active_profile': active_profile,
                'active_group': active_group, 'comments': comments}

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
