from django.db import models
from django.contrib.auth.models import User


class MealPlan(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_plan'
    )

    def __str__(self):
        return f'Meal plan {self.pk}'


class MealType(models.Model):
    meal_type_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.meal_type_name}'


class Meal(models.Model):
    meal_name = models.CharField(max_length=50)
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name='meal'
    )
    day = models.DateTimeField()
    meal_type = models.ForeignKey(
        MealType,
        on_delete=models.CASCADE,
        related_name='meal_type'
    )

    def __str__(self):
        return f'{self.meal_name}'
