# Imports:
# 3rd party:
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.forms import formset_factory
from django.contrib import messages

# Internal
from .forms import MealForm, MealPlanForm
from .models import MealPlan, Meal, MealType


class Index(View):
    """
    Displays the home page
    """
    def get(self, request):
        """Renders the home page
        Args:
            request (object): HTTP request object
        Returns:
            method: renders home page
        """
        return render(request, 'index.html')


class PickStartDate(LoginRequiredMixin, View):
    """
    A view for picking the start date for the mealplan
    """
    def get(self, request):
        """Renders the form to pick meal plan start date
        Args:
            request (object): HTTP request object
        Returns:
            method: renders pick_start_date.html
        """
        return render(
            request,
            'pick_start_date.html',
            {
                'meal_plan_form': MealPlanForm()
            }
        )

    def post(self, request):
        """Takes input from meal_plan_form and if the form is valid
        creates new meal plan else renders the form again
        Args:
            request (object): HTTP request object
        Returns:
            method: redirects to add meal view
        """
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
    """
    A view for adding meals into the meal plan
    """
    def get(self, request):
        """Renders the formset for adding meals to the meal plan
        Args:
            request (object): HTTP request object
        Returns:
            method: renders formset for adding meals
        """
        try:
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
        except Exception as error:
            messages.error(request, f'An Error occured: {error}')
            return redirect('home')

    def post(self, request):
        """Takes input from meal formset and if the formset is valid
        creates new meals in database
        Args:
            request (object): HTTP request object
        Returns:
            method: redirects meal plans view
        """
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
                if meal_name is None:
                    meal_name = ''
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
            messages.success(request, 'You have created a new mealplan.')
            return redirect('meal_plans')


class ViewMealPlans(LoginRequiredMixin, generic.list.ListView):
    """
    A view to display all meal plans of a user, paginated by 1
    """
    model = MealPlan
    template_name = 'meal_plans.html'
    paginate_by = 1

    def get_queryset(self):
        """
        Returns:
            list: list of all mealplans by a specific user orderd by start date
        """
        return MealPlan.objects.filter(user=self.request.user).order_by(
            'day_1'
        )


class EditMealPlan(LoginRequiredMixin, View):
    """
    A view for editing meal plans
    """
    def get(self, request, **kwargs):
        """Renders a formset prefilled with initial data for meal_plan_id
        If the user requesting the edit is not the same as meal_plan.user
        (user doesn't own the meal_plan) redirects to meal_plans view
        Args:
            request (object): HTTP request object
            **meal_plan_id (int): pk of meal plan being edited
        Returns:
            method: renders edit_meal_plan form
        """
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)

        if request.user == meal_plan.user:
            # code on how to use inital data was inspired by this
            # https://stackoverflow.com/a/15853036
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
        else:
            messages.info(request, 'You can only edit your own mealplans')
            return redirect('meal_plans')

    def post(self, request, **kwargs):
        """Takes input from meal formset and if the formset is valid
        creates updates meals in database
        Args:
            request (object): HTTP request object
        Returns:
            method: redirects meal plans view
        """
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        meals = Meal.objects.filter(meal_plan=meal_plan).order_by('pk')
        meals_formset = formset_factory(MealForm, extra=21)
        formset = meals_formset(request.POST)
        if formset.is_valid():
            i = 0
            for form in formset:
                meal = meals[i]
                meal_name = form.cleaned_data.get('meal_name')
                meal.meal_name = meal_name
                meal.save()
                i += 1
            messages.success(request, 'Your mealplan was successfully updated')
            return redirect('meal_plans')
        else:
            messages.error(request, 'Ooops, something went wrong! Try again.')
            return redirect('meal_plans')


class DeleteMealPlan(LoginRequiredMixin, View):
    """
    A view to delete meal plans
    """
    def post(self, request, **kwargs):
        """Deletes the sellected meal plan
        Args:
            request (object): HTTP request object
            **meal_plan_id (int): pk of meal plan being deleted
        Returns:
            method: redirects to meal_plans
        """
        meal_plan_id = self.kwargs['meal_plan_id']
        meal_plan = MealPlan.objects.get(pk=meal_plan_id)
        meal_plan.delete()
        messages.success(request, 'Mealplan succesfully deleted!')
        return redirect('meal_plans')

    def get(self, request, **kwargs):
        """
        Handles deleting by get method
        Returns:
            method: redircets to meal_plans
        """
        messages.warning(
            request,
            'Deleting meal plans by URL is not allowed!'
        )
        return redirect('meal_plans')
