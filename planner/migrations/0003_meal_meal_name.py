# Generated by Django 3.2.8 on 2021-10-24 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_auto_20211024_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='meal_name',
            field=models.CharField(default='m', max_length=50),
            preserve_default=False,
        ),
    ]
