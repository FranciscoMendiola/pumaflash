from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from APP.models import Comment

class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, id):
        comment,profile = self.__validate_request(request, id)
        comment.delete()
        
        return redirect('profile', id=profile.id_profile)
        
    def __validate_request(self, request, id):
        # verificamos que el perfil solicitado existe
        comment = get_object_or_404(Comment, id_comment=id)
        profile = comment.id_receiver

        # Validar permisos
        if request.user.is_staff and profile.id_group.id_admin != request.user:
            raise HttpResponse(
                "El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            raise HttpResponse("No tienes permisos para eliminar comentarios", status=404)

        return comment, profile
    