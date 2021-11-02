from django.shortcuts import render, redirect
from django.views import View, generic
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
            day_1 = meal_plan_form.cleaned_data.get('day_1')
            meal_plan = MealPlan(
                user=user,
                day_1=day_1,
            )
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
        meals = formset_factory(MealForm, extra=21)
        formset = meals()
        return render(
            request,
            'add_meal_plan.html',
            {
                'meal_plan': meal_plan,
                'formset': formset,
            }
        )

    def post(self, request):
        meal_plan_id = request.session.get('meal_plan_id')
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        days = [
            meal_plan.day_1,
            meal_plan.day_2,
            meal_plan.day_3,
            meal_plan.day_4,
            meal_plan.day_5,
            meal_plan.day_6,
            meal_plan.day_7
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
            return redirect('meal_plans')


class ViewMealPlans(generic.list.ListView):
    model = MealPlan
    template_name = 'meal_plans.html'
    paginate_by = 1

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user).order_by(
            'day_1'
        )


class EditMealPlan(View):
   
    def get(self, request, **kwargs):
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)

        # code on how to use inital data was inspired by this https://stackoverflow.com/a/15853036
        meals = Meal.objects.filter(meal_plan=meal_plan_id)
        meals_formset = formset_factory(MealForm, extra=21, max_num=21)
        initial_data = []
        for meal in meals:
            initial_data.append({'meal_name': meal.meal_name})
        formset = meals_formset(initial=initial_data)
        return render(
            request,
            'edit_meal_plan.html',
            {
                'meal_plan_id': meal_plan_id,
                'meal_plan': meal_plan,
                'formset': formset,
            }
        )

    def post(self, request, **kwargs):
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        meals = Meal.objects.filter(meal_plan=meal_plan).order_by('pk')
        start_id = meals[1].pk
        meals_formset = formset_factory(MealForm, extra=21)
        formset = meals_formset(request.POST)
        if formset.is_valid():
            idx = 0
            for form in formset:
                primary_key = start_id + idx
                meal = Meal.objects.get(pk=primary_key)
                meal_name = form.cleaned_data.get('meal_name')
                meal.meal_name = meal_name
                meal.save()
            return redirect('meal_plans')


class DeleteMealPlan(View):
    
    def post(self, request, **kwargs):
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        meal_plan.delete()
        return redirect('meal_plans')
