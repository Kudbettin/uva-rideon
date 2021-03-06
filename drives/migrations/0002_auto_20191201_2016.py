# Generated by Django 2.2.7 on 2019-12-01 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drives', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='riderreview',
            name='by',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='rider_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='riderreview',
            name='drive',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='drives.Drive'),
        ),
        migrations.AddField(
            model_name='riderreview',
            name='of',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='rider_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rideapplication',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rideapplication',
            name='waypoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waypoint', to='drives.Location'),
        ),
        migrations.AddField(
            model_name='driverreview',
            name='by',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='driver_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='driverreview',
            name='drive',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='drives.Drive'),
        ),
        migrations.AddField(
            model_name='driverreview',
            name='of',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='driver_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drive',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drive',
            name='end_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_location', to='drives.Location'),
        ),
        migrations.AddField(
            model_name='drive',
            name='passengers',
            field=models.ManyToManyField(blank=True, related_name='passengers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='drive',
            name='requestList',
            field=models.ManyToManyField(blank=True, related_name='requestList', to='drives.RideApplication'),
        ),
        migrations.AddField(
            model_name='drive',
            name='start_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_location', to='drives.Location'),
        ),
        migrations.AddField(
            model_name='drive',
            name='waypointList',
            field=models.ManyToManyField(blank=True, related_name='waypointList', to='drives.Location'),
        ),
    ]
