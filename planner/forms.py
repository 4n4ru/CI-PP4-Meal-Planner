from django import forms
from .models import MealPlan, MealType, Meal


class DateInput(forms.DateInput):
    input_type = 'date'


class MealPlanForm(forms.ModelForm):
    
    class Meta:
        model = MealPlan
        fields = ('day_1',)
        widgets = {
            'day_1': DateInput(),
        }


class MealTypeForm(forms.ModelForm):

    class Meta:
        model = MealType
        fields = ('meal_type_name',)


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ('meal_name',)
