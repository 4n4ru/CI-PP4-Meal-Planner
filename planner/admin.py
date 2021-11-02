from django.contrib import admin
from .models import MealPlan, MealType, Meal


# Register your models here.
@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_filter = ['user', 'day_1']
    list_display = ['user', 'day_1', 'pk']
    search_fields = ['user']


@admin.register(MealType)
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ['meal_type_name']
    list_filter = ['meal_type_name']


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['meal_name', 'meal_plan', 'day', 'meal_type', 'pk']
    list_filter = ['meal_name', 'meal_plan', 'day', 'meal_type']
    search_fields = ['meal_name', 'meal_plan', 'day', 'meal_type']
