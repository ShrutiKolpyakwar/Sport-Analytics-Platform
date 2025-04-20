from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sport = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.sport}"

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    matches_played = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    skill_level = models.IntegerField(default=0) 


    def __str__(self):
        return f"{self.name} ({self.team.name})"
