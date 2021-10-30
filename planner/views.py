from datetime import timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.forms import formset_factory
from .forms import MealForm, MealPlanForm
from .models import MealPlan, Meal, MealType


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
            meal_plan = MealPlan(user=user, start_date=start_date)
            meal_plan.save()
            request.session['meal_plan_id'] = meal_plan.pk
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
        meal_plan_id = request.session.get('meal_plan_id')
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        day1 = meal_plan.start_date
        day2 = day1 + timedelta(days=1)
        day3 = day1 + timedelta(days=2)
        day4 = day1 + timedelta(days=3)
        day5 = day1 + timedelta(days=4)
        day6 = day1 + timedelta(days=5)
        day7 = day1 + timedelta(days=6)
        meals = formset_factory(MealForm, extra=21)
        formset = meals()
        return render(
            request,
            'add_meal_plan.html',
            {
                'day1': day1,
                'day2': day2,
                'day3': day3,
                'day4': day4,
                'day5': day5,
                'day6': day6,
                'day7': day7,
                'formset': formset,
            }
        )

    def post(self, request):
        meal_plan_id = request.session.get('meal_plan_id')
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        start_date = meal_plan.start_date
        days = [
            start_date,
            start_date + timedelta(days=1),
            start_date + timedelta(days=2),
            start_date + timedelta(days=3),
            start_date + timedelta(days=4),
            start_date + timedelta(days=5),
            start_date + timedelta(days=6),
        ]
        meals = formset_factory(MealForm, extra=21)
        formset = meals(request.POST)
        if formset.is_valid():
            idx = 0
            for form in formset:
                meal_name = form.cleaned_data.get('meal_name')
                meal_day = days[idx % 7]
                if idx < 7:
                    meal_type = MealType.objects.get(
                        meal_type_name='Breakfast'
                    )
                elif idx < 14:
                    meal_type = MealType.objects.get(meal_type_name='Lunch')
                else:
                    meal_type = MealType.objects.get(meal_type_name='Dinner')
                meal = Meal(
                    meal_name=meal_name,
                    meal_plan=meal_plan,
                    meal_type=meal_type,
                    day=meal_day
                )
                meal.save()
                idx += 1
            return redirect('home')
