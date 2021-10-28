from django import forms
from .models import MealPlan, MealType, Meal


class DateInput(forms.DateInput):
    input_type = 'date'


class MealPlanForm(forms.ModelForm):

    class Meta:
        model = MealPlan
        fields = ('start_date',)
        widgets = {
            'made_on': DateInput(),
        }


class MealTypeForm(forms.ModelForm):

    class Meta:
        model = MealType
        fields = ('meal_type_name',)


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ('meal_name', 'meal_plan', 'day', 'meal_type')
