from django.views import View
from django.shortcuts import render
from APP.models import Profile, User

class VotacionesView(View):
    categorias = ['A', 'B', 'C', 'D', 'E']

    def get(self, request):
        # Mostrar todos los estudiantes sin filtrar por categoría ni código
        estudiantes = User.objects.all()

        categoria_actual = request.GET.get('categoria', 'A')
        try:
            index_actual = self.categorias.index(categoria_actual)
        except ValueError:
            index_actual = 0

        next_index = (index_actual + 1) % len(self.categorias)

        context = {
            'students': estudiantes,
            'current_category': f'{self.categorias[index_actual]}',
            'next_category': self.categorias[next_index],
        }

        return render(request, 'votaciones.html', context)
