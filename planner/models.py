from django.db import models
from django.contrib.auth.models import User


class MealPlan(models.Model):
    start_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MealType(models.Model):
    meal_type_name = models.CharField(max_length=50)


class Meal(models.Model):
    meal_name = models.CharField(max_length=50)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    day = models.DateField()
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
