# APP/views/codes.py

import random
import string
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from APP.models import Group, Profile


def generar_codigo_unico():
    while True:
        codigo = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6))
        if not Group.objects.filter(code=codigo).exists():
            return codigo


class GeneratorView(View):
    def get(self, request):
        grupos = Group.objects.filter(id_admin=request.user)
        return render(request, 'generator.html', {'grupos': grupos})

    def post(self, request):
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            codigo = generar_codigo_unico()
            grupo = Group.objects.create(
                group_name=nombre,
                code=codigo,
                id_admin=request.user
            )
            return redirect('generator')
        else:
            messages.error(request, 'El nombre del grupo es obligatorio.')
            return redirect('generator')


class GroupsView(View):
    def get(self, request):
        # Si el usuario ya tiene un grupo, redirigir automáticamente
        if Profile.objects.filter(id_user=request.user).exists():
            grupo = Profile.objects.filter(
                id_user=request.user).first().id_group
            return redirect('home', code=grupo.code)

        return render(request, 'groups.html')

    def post(self, request):
        code = request.POST.get('code', '').strip().upper()
        try:
            grupo = Group.objects.get(code=code)

            # Validar si ya tiene un grupo (no permitir cambiar de grupo)
            if Profile.objects.filter(id_user=request.user).exists():
                messages.warning(
                    request, 'Ya perteneces a un grupo. No puedes cambiar de grupo.')
                perfil = Profile.objects.filter(id_user=request.user).first()
                return redirect('home', code=perfil.id_group.code)

            # Crear perfil si aún no tiene
            Profile.objects.create(id_user=request.user,
                                   id_group=grupo, description='Bienvenido(a) a mi perfil, soy miembro de PumaFlash')
            return redirect('home', code=grupo.code)
        except Group.DoesNotExist:
            messages.error(
                request, 'Código inválido. Verifica con tu profesor.')
            return redirect('groups')
