# Imports:
# 3rd party:
from django.urls import path
# Internal:
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('sample_meal_plan', views.Sample.as_view(), name='sample_meal_plan'),
    path('add', views.AddMeal.as_view(), name='add_meal'),
    path('pick_date', views.PickStartDate.as_view(), name='pick_start_date'),
    path('view_meal_plans', views.ViewMealPlans.as_view(), name='meal_plans'),
    path('edit_meal_plan/<int:meal_plan_id>', views.EditMealPlan.as_view(),
         name='edit_plan'),
    path('delete_meal_plan/<int:meal_plan_id>', views.DeleteMealPlan.as_view(),
         name='delete_plan'),
]
