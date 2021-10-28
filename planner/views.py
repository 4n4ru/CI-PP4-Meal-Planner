from django.shortcuts import render, redirect
from django.views import View, generic
from .forms import MealForm, MealPlanForm
from .models import MealPlan
from django.contrib.auth.models import User


class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class PickStartDate(View):
    def get(self, request):
        return render(
            request,
            'pick_start_date.html',
            {
                'meal_plan_form': MealPlanForm()
            }
        )

    def post(self, request):
        meal_plan_form = MealPlanForm(data=request.POST)
        if meal_plan_form.is_valid():
            user = request.user
            start_date = meal_plan_form.cleaned_data.get('start_date')
            MealPlan(user=user, start_date=start_date).save()
            return redirect('add_meal')
        else:
            meal_plan_form = MealPlanForm()
            return render(
                request,
                'pick_start_date.html',
                {
                    'meal_plan_form': meal_plan_form
                }
            )


class AddMeal(View):

    def get(self, request):
        return render(
            request,
            'add_meal_plan.html',
            {
                'meal_form': MealForm(),
            }
        )
