# APP/views/codes.py

import random, string
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from APP.models import Group

def generar_codigo_unico():
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
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
            messages.success(request, f'Grupo \"{grupo.group_name}\" creado con código: {codigo}')
            return redirect('generator')
        else:
            messages.error(request, 'El nombre del grupo es obligatorio.')
            return redirect('generator')

class GroupsView(View):
    def get(self, request):
        return render(request, 'groups.html')

    def post(self, request):
        code = request.POST.get('code', '').strip().upper()
        try:
            grupo = Group.objects.get(code=code)
            messages.success(request, f'¡Bienvenido al grupo \"{grupo.group_name}\"!')
            return redirect('home', code=grupo.code)
        except Group.DoesNotExist:
            messages.error(request, 'Código inválido. Verifica con tu profesor.')
            return redirect('groups')
