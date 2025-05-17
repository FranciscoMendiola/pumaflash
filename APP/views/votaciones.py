from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from APP.models import Group, Profile, User, Category, Vote

def get_next_category_id(current_id):
    categorias = list(Category.objects.all().order_by('id_category'))
    for i, cat in enumerate(categorias):
        if cat.id_category == int(current_id) and i + 1 < len(categorias):
            return categorias[i + 1].id_category
    return categorias[0].id_category  # volver al principio si ya estás en la última

class VotacionesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        # Obtener el grupo del usuario (asumiendo que siempre tiene uno)
        group = get_object_or_404(Group, profile__id_user=user)
        
        current_category_id = request.GET.get('categoria')
        if current_category_id:
            current_category = get_object_or_404(Category, pk=current_category_id)
        else:
            current_category = Category.objects.first()
        
        # Obtener los estudiantes del grupo, excepto el usuario actual
        students = User.objects.filter(profile__id_group=group).exclude(id=user.id)
        
        # Verificar si el usuario ya votó en esta categoría
        vote_exists = Vote.objects.filter(
            voting_user=user,
            category=current_category
        ).exists()
        
        context = {
            "students": students,
            "current_category": current_category,
            "next_category": get_next_category_id(current_category.id_category),
            "has_voted": vote_exists,
        }

        votos_totales = Vote.objects.values(
            'category__name',                     # nombre de la categoría
            'voted_user__first_name',
            'voted_user__last_name',
            'voted_user__id'
        ).annotate(total=Count('id_vote')).order_by('category__name', '-total')


        context['ranking'] = votos_totales #Tomar en cuenta para los premios

        return render(request, "votaciones.html", context)

    def post(self, request):
        user = request.user
        group = get_object_or_404(Group, profile__id_user=user)

        current_category_id = request.POST.get('categoria')
        if current_category_id:
            current_category = get_object_or_404(Category, pk=current_category_id)
        else:
            current_category = Category.objects.first()

        # Verificar si ya votó en esta categoría (previene doble voto)
        vote_exists = Vote.objects.filter(
            voting_user=user,
            category=current_category
        ).exists()

        if not vote_exists:
            voted_user_id = request.POST.get("voted_user_id")
            voted_user = get_object_or_404(User, pk=voted_user_id)

            Vote.objects.create(
                voted_user=voted_user,
                voting_user=user,
                category=current_category
            )

        # Redirigir a la siguiente categoría
        next_category_id = get_next_category_id(current_category.id_category)
        return redirect(f"{request.path}?categoria={next_category_id}")
