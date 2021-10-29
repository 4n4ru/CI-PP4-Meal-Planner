from . import views
from django.urls import path

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('add', views.AddMeal.as_view(), name='add_meal'),
    path('pick_date', views.PickStartDate.as_view(), name='pick_start_date'),
]
