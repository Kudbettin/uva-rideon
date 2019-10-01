# Generated by Django 2.1.3 on 2019-10-01 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_time', models.DateTimeField()),
                ('description', models.TextField()),
                ('min_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_cost', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_method', models.CharField(max_length=100)),
                ('max_passengers', models.IntegerField()),
                ('car_description', models.TextField()),
                ('luggage_description', models.TextField(blank=True, null=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('dropoff_in_drive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drives.Drive')),
            ],
        ),
        migrations.AddField(
            model_name='drive',
            name='end_location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='end_location', to='drives.Location'),
        ),
        migrations.AddField(
            model_name='drive',
            name='passengers',
            field=models.ManyToManyField(blank=True, related_name='passengers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drive',
            name='start_location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='start_location', to='drives.Location'),
        ),
    ]
