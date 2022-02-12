from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class MealPlan(models.Model):
    day_1 = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_plan'
    )

    @property
    def day_2(self):
        return self.day_1 + timedelta(days=1)

    @property
    def day_3(self):
        return self.day_1 + timedelta(days=2)

    @property
    def day_4(self):
        return self.day_1 + timedelta(days=3)

    @property
    def day_5(self):
        return self.day_1 + timedelta(days=4)

    @property
    def day_6(self):
        return self.day_1 + timedelta(days=5)

    @property
    def day_7(self):
        return self.day_1 + timedelta(days=6)

    def __str__(self):
        return f'Meal plan {self.pk}'


class MealType(models.Model):
    meal_type_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.meal_type_name}'


class Meal(models.Model):
    meal_name = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        default=''
    )
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
