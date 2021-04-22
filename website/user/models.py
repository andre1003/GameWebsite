from django.db import models
from django.contrib.auth.models import User
import uuid


# Partida
class Group(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# Jogador
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    age = models.CharField(max_length=3)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.first_name


# Todas as escolhas de uma única partida
class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    match_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=20)
    hits = models.PositiveIntegerField()
    mistakes = models.PositiveIntegerField()
    individual_feedback = models.TextField()
    player = models.ForeignKey(Player, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.match_id)


# Uma decisão
class Decision(models.Model):
    decision = models.CharField(max_length=250)
    concept = models.CharField(max_length=150)
    is_mistake = models.BooleanField()
    choice = models.ForeignKey(Match, on_delete=models.PROTECT)

    def __str__(self):
        return self.decision