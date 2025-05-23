from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from APP.models import Group, Profile, User, Category, Vote

def get_prev_category_id(current_id):
    categorias = list(Category.objects.all().order_by('id_category'))
    for i, cat in enumerate(categorias):
        if cat.id_category == int(current_id) and i - 1 >= 0:
            return categorias[i - 1].id_category
    return categorias[-1].id_category  # volver al final si ya estás en la primera


def get_next_category_id(current_id):
    categorias = list(Category.objects.all().order_by('id_category'))
    for i, cat in enumerate(categorias):
        if cat.id_category == int(current_id) and i + 1 < len(categorias):
            return categorias[i + 1].id_category
    return categorias[0].id_category  # volver al principio si ya estás en la última

class VotacionesView(LoginRequiredMixin, View):
    def get(self, request, code):
        active_group, active_profile = self.__validate_request(request, code)

        if not Category.objects.exists():
            return render(request, "noCategorias.html")

        current_category_id = request.GET.get('categoria')
        if current_category_id:
            current_category = get_object_or_404(Category, pk=current_category_id)
        else:
            current_category = Category.objects.first()

        students = User.objects.filter(profile__id_group=active_group, is_staff=False)

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
            "code": code,
            "group": active_group,
            "active_group": active_group,
            "active_profile": active_profile,
            "students": students,
            "current_category": current_category,
            "next_category": get_next_category_id(current_category.id_category),
            "prev_category": get_prev_category_id(current_category.id_category),
            "has_voted": vote_exists,
            "ranking": votos_totales,
        }

        return render(request, "votaciones.html", context)

    def post(self, request, code):
        active_group, active_profile = self.__validate_request(request, code)

        if not Category.objects.exists():
            return render(request, "noCategorias.html")

        current_category_id = request.POST.get('categoria')
        if current_category_id:
            current_category = get_object_or_404(Category, pk=current_category_id)
        else:
            current_category = Category.objects.first()

        vote_exists = Vote.objects.filter(
            voting_user=request.user,
            category=current_category
        ).exists()

        if not vote_exists:
            voted_user_id = request.POST.get("voted_user_id")
            voted_user = get_object_or_404(User, pk=voted_user_id)

            Vote.objects.create(
                voted_user=voted_user,
                voting_user=request.user,
                category=current_category
            )

        return redirect(f"/home/{code}/votaciones/?categoria={current_category.id_category}")

    def __validate_request(self, request, code):
        active_group = get_object_or_404(Group, code=code)
        active_profile = None

        if request.user.is_staff and active_group.id_admin != request.user:
            return HttpResponse("El usuario no es administrador del grupo", status=403)
        elif not request.user.is_staff:
            active_profile = get_object_or_404(Profile, id_group=active_group, id_user=request.user)

        return active_group, active_profile
