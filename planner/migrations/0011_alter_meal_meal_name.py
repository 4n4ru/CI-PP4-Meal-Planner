# Generated by Django 3.2.8 on 2022-02-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0010_alter_meal_meal_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
