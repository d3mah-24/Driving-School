from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Car(models.Model):
    question = models.CharField(max_length=1000)
    choose = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.id)


class Moto(models.Model):
    question = models.CharField(max_length=1000)
    choose = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.id)


class Auto(models.Model):
    question = models.CharField(max_length=1000)
    choose = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.id)


class points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1000)
    point = models.IntegerField()
    def __str__(self):
        return self.type
