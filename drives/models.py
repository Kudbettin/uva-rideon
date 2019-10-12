from django.db import models
from users.models import CustomUser

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
    # Why is this one to one?
    # start_location  = models.OneToOneField(Location, on_delete = models.CASCADE, related_name="start_location")
    # end_location    = models.OneToOneField(Location, on_delete = models.CASCADE, related_name="end_location")    
    start_location  = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="start_location")
    end_location    = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="end_location")
    title           = models.CharField(max_length=100)
    driver          = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="driver", null=True)
    date_time       = models.DateTimeField()
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
	    return Location
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