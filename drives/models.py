from django.db import models
from users.models import CustomUser
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator

'''
A map location, likely pulled from Google APIs
'''
class Location(models.Model):
    location = models.TextField()
    coordinates_x = models.FloatField(default=0)
    coordinates_y = models.FloatField(default=0)
    dropoff_in_drive = models.ForeignKey('Drive', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

'''
A trip that will be undertaken at a concrete point in time.
Differs from a 'ride' in that a 'ride' is a request for a drive.
'''
class Drive(models.Model):
    start_street_number = models.TextField(null=True, blank=True)
    start_route     = models.TextField(null=True, blank=True) 
    start_locality  = models.TextField(null=True, blank=True)
    start_administrative_area_level_1 = models.TextField(null=True, blank=True)
    start_country   = models.TextField(null=True, blank=True)
    start_postal_code = models.TextField(null=True, blank=True)
    end_street_number = models.TextField(null=True, blank=True)
    end_route     = models.TextField(null=True, blank=True) 
    end_locality  = models.TextField(null=True, blank=True)
    end_administrative_area_level_1 = models.TextField(null=True, blank=True)
    end_country   = models.TextField(null=True, blank=True)
    end_postal_code = models.TextField(null=True, blank=True)
    title           = models.CharField(max_length=100)
    driver          = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="driver", null=True)
    # date_time       = models.DateTimeField()
    date            = models.DateField()
    time            = models.TimeField()
    description     = models.TextField()
    passengers      = models.ManyToManyField(CustomUser, related_name="passengers", blank=True)
    min_cost        = models.DecimalField(max_digits=5, decimal_places=2)
    max_cost        = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method  = models.CharField(max_length=100)
    max_passengers  = models.IntegerField()
    car_description = models.TextField()
    luggage_description = models.TextField(null=True, blank=True)
	
	# Override the delete method so the start and end locations will be deleted
	# @Override
    def delete(self, *args, **kwargs):
        self.start_location.delete()
        self.end_location.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
	
    def get_dropoffs(self):
	    return Location.objects.filter()
    '''
    Adds a passenger to the drive if there is space, otherwise does not
	
	@param passenger the passenger being added to the drive
	@return a boolean value indicating if the passenger was added or not
	'''
    def add_passenger(self, passenger):
	    if self.passengers.count() >= self.max_passengers:
		    return False
			
	    self.passengers.add(passenger)
	    return True
		
def create_drive(username_str, start_location_str="Start Location", end_location_str="End Location", title_str="Title", description_str="Description"):
	start_location = Location.objects.create(location = start_location_str)
	end_location   = Location.objects.create(location = end_location_str)
	
	driver = CustomUser.objects.create(username=username_str)
	
	drive = Drive.objects.create(start_location=start_location, end_location=end_location, title=title_str, 
										driver=driver, date_time=timezone.now(), description=description_str, min_cost=2,
										max_cost=10, payment_method="payment", max_passengers=4, car_description="mycar")
										
	dropoff = Location.objects.create(location = "dropoff", dropoff_in_drive=drive)
	
	return start_location, end_location, driver, drive, dropoff
class DriverReview(models.Model):
    by = models.OneToOneField(CustomUser, on_delete = models.SET_NULL, related_name="driver_by", null=True)
    of = models.OneToOneField(CustomUser, on_delete = models.SET_NULL, related_name="driver_of", null=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    drive = models.OneToOneField(Drive, on_delete = models.CASCADE)

class RiderReview(models.Model):
    by = models.OneToOneField(CustomUser, on_delete = models.SET_NULL, related_name="rider_by", null=True)
    of = models.OneToOneField(CustomUser, on_delete = models.SET_NULL, related_name="rider_of", null=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    drive = models.OneToOneField(Drive, on_delete = models.CASCADE)
