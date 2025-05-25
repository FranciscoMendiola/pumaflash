from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from APP.models import Group, Profile, User, Category, Vote, Award
from django.http import HttpResponse


def get_prev_category_id(current_id):
    categorias = list(Category.objects.all().order_by('id_category'))
    for i, cat in enumerate(categorias):
        if cat.id_category == int(current_id) and i - 1 >= 0:
            return categorias[i - 1].id_category
    # volver al final si ya estás en la primera
    return categorias[-1].id_category


def get_next_category_id(current_id):
    categorias = list(Category.objects.all().order_by('id_category'))
    for i, cat in enumerate(categorias):
        if cat.id_category == int(current_id) and i + 1 < len(categorias):
            return categorias[i + 1].id_category
    # volver al principio si ya estás en la última
    return categorias[0].id_category


def actualizaPremios(voto, active_group):
    '''
    Función que actualiza los premios del más votado por categoría
    '''

    category = voto.category
    votado = voto.voted_user

    # Si no hay un premio de esta categoría y el grupo del voto entonces se crea uno
    if not Award.objects.filter(id_category=category, id_group=active_group).exists():
        id_winner = Profile.objects.get(id_user=votado, id_group=active_group)
        Award.objects.create(id_winner=id_winner,
                             id_category=category, id_group=active_group)
    else:
        # Si ya hay uno o más premios de esta categoría y grupo tomamos el que sea de esos
        premioActual = Award.objects.filter(
            id_category=category, id_group=active_group).first()
        # Tomamos el user del ganador actual
        id_winner = premioActual.id_winner.id_user

        # Contamos el número de votos que tiene este ganador
        numVotosGanador = Vote.objects.filter(
            voted_user=id_winner, category=category).count()

        # Contamos el número de votos que tiene el recien votado
        numVotosCandidato = Vote.objects.filter(
            voted_user=votado, category=category).count()

        # Casos del sencillo al largo
        # 1.- Si el candidato no toma la delantera con este voto no hacemos nada
        if numVotosCandidato < numVotosGanador:
            return
        # 2.- Si el candidato empata a los ganadores le creamos un premio
        if numVotosCandidato == numVotosGanador:
            id_winner = Profile.objects.get(
                id_user=votado, id_group=active_group)
            Award.objects.create(id_winner=id_winner,
                                 id_category=category, id_group=active_group)
            return
        # 3.- Si el candidato supera al ganador actual, entonces borramos todos los premios de esta categoría y grupo
        # y creamos uno nuevo con el nuevo ganador
        if numVotosCandidato > numVotosGanador:
            # Este if ya no es necesario por tricotomía pero lo dejo por el flujo más sencillo
            # Borramos todos los premios de esta categoría y grupo
            Award.objects.filter(
                id_category=category, id_group=active_group).delete()
            # Creamos el nuevo premio
            id_winner = Profile.objects.get(
                id_user=votado, id_group=active_group)
            Award.objects.create(id_winner=id_winner,
                                 id_category=category, id_group=active_group)


class VotacionesView(LoginRequiredMixin, View):
    def get(self, request, code):
        active_group, active_profile = self.__validate_request(request, code)

        if Category.objects.exists():
            current_category_id = request.GET.get('categoria')
            if current_category_id:
                current_category = get_object_or_404(
                    Category, pk=current_category_id)
            else:
                current_category = Category.objects.first()

            students = User.objects.filter(
                profile__id_group=active_group, is_staff=False)

            # Quitamos al estudiante actual, pero como @dannaliz está usando User en lugar de Profile entonces primero obtenemos el
            # user del active_profile y ya luego el id del profile para quitarlo
            if active_profile:
                students = students.exclude(id=active_profile.id_user.id)

            vote_exists = request.user.is_staff or Vote.objects.filter(
                voting_user=request.user,
                category=current_category
            ).exists()

            votos_totales = Vote.objects.values(
                'category__name',
                'voted_user__first_name',
                'voted_user__last_name',
                'voted_user__id'
            ).annotate(total=Count('id_vote')).order_by('category__name', '-total')

            context = {
                'active_profile': active_profile,  # Requerido por el navbar
                "active_group": active_group,
                "students": students,
                "current_category": current_category,
                "next_category": get_next_category_id(current_category.id_category),
                "prev_category": get_prev_category_id(current_category.id_category),
                "has_voted": vote_exists,
                "ranking": votos_totales,
            }
        else:
            context = {
                'active_profile': active_profile,  # Requerido por el navbar
                "active_group": active_group,
                "students": [],
                "current_category": None,
                "next_category": None,
                "prev_category": None,
                "has_voted": False,
                "ranking": [],
            }
        return render(request, "votaciones.html", context)

    def post(self, request, code):
        active_group, active_profile = self.__validate_request(request, code)

        if not Category.objects.exists():
            return render(request, "noCategorias.html")

        current_category_id = request.POST.get('categoria')
        if current_category_id:
            current_category = get_object_or_404(
                Category, pk=current_category_id)
        else:
            current_category = Category.objects.first()

        vote_exists = Vote.objects.filter(
            voting_user=request.user,
            category=current_category
        ).exists()

        if not vote_exists:
            voted_user_id = request.POST.get("voted_user_id")
            voted_user = get_object_or_404(User, pk=voted_user_id)

            voto = Vote.objects.create(
                voted_user=voted_user,
                voting_user=request.user,
                category=current_category
            )
            actualizaPremios(voto, active_group)

        return redirect(f"/votaciones/{code}/?categoria={current_category.id_category}")

    def __validate_request(self, request, code):
        active_group = get_object_or_404(Group, code=code)
        active_profile = None

        if request.user.is_staff and active_group.id_admin != request.user:
            return HttpResponse("El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            active_profile = get_object_or_404(
                Profile, id_group=active_group, id_user=request.user)

        return active_group, active_profile
