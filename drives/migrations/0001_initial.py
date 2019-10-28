# Generated by Django 2.2.5 on 2019-10-28 05:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField()),
                ('min_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_method', models.CharField(max_length=100)),
                ('max_passengers', models.IntegerField()),
                ('car_description', models.TextField()),
                ('luggage_description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='Listed', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DriverReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('coordinates_x', models.FloatField(default=0)),
                ('coordinates_y', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RiderReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
    ]
