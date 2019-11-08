from django.conf import settings
import django.core.validators
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
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to=settings.AUTH_USER_MODEL)),
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
                ('by', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='driver_by', to=settings.AUTH_USER_MODEL)),
                ('drive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='drives.Drive')),
                ('of', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='driver_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('coordinates_x', models.FloatField(default=0)),
                ('coordinates_y', models.FloatField(default=0)),
                ('dropoff_in_drive', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='drives.Drive')),
            ],
        ),
        migrations.CreateModel(
            name='RideApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('waypoint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='waypoint', to='drives.Location')),
                ('dropoff_in_drive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drives.Drive')),
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
                ('by', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='rider_by', to=settings.AUTH_USER_MODEL)),
                ('drive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='drives.Drive')),
                ('of', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='rider_of', to=settings.AUTH_USER_MODEL)),
            ],
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
    ]
