from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=80, unique=True)
    img_url = models.ImageField(
        upload_to='img/usuarios', default='img/usuarios/default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name', 'password', 'is_staff']

    def __str__(self):
        return self.email


class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    group_name = models.CharField(max_length=50)
    img_url = models.ImageField(
        upload_to='img/grupos', default='img/grupos/default.png')

    def __str__(self):
        return self.group_name + " - " + self.code


class Profile(models.Model):
    id_profile = models.AutoField(primary_key=True)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(
        default="Bienvenido(a) a mi perfil, soy miembro de PumaFlash")

    class Meta:
        unique_together = ('id_group', 'id_user')

    def __str__(self):
        return self.id_user.name + " - " + self.id_group.group_name


class Comment(models.Model):
    id_comment = models.AutoField(primary_key=True)
    id_receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments_received')
    id_sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments_sent')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_sender.id_user.name + " - " + self.id_receiver.id_user.name


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=False)
    img_url = models.ImageField(
        upload_to='img/categorias', default='img/categorias/default.png')

    def __str__(self):
        return self.name


class Award(models.Model):
    id_award = models.AutoField(primary_key=True)
    id_winner = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_winner.id_user) + " - " + str(self.id_category) + " - " + str(self.id_group)


class Vote(models.Model):
    id_vote = models.AutoField(primary_key=True)
    voted_user = models.ForeignKey(
        User, related_name='votes_received', on_delete=models.CASCADE)
    voting_user = models.ForeignKey(
        User, related_name='votes_cast', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote from {self.voting_user.username} to {self.voted_user.username} in {self.category.name}"
