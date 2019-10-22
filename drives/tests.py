from django.test import TestCase
from drives.models import *
from users.models import CustomUser
from django.utils import timezone
from drives.views import *
from RideOn.SeleniumTester import *

class DriveModelTester(TestCase):
	# Setup for all tests
	# Creates a sample drive with default values and none of the optional values
	def setUp(self):		
		self.start_location, self.end_location, self.driver, self.drive, self.dropoff = create_drive(
			"Name", start_location_str = "Start Location", end_location_str = "End Location", 
			title_str = "Drive Title", description_str = "Drive Description")
		
	# Verifies that when the drive is deleted, the associated location
	# objects get deleted as well
	def testDriveDeletionOnLocations(self):	
		self.drive.delete()
		self.assertEqual(Location.objects.all().count(), 0)
		
	# Verifies that when the start location is deleted,
	#  the associated drive is as well deleted
	def testStartLocationDeletion(self):
		Location.objects.get(location="Start Location").delete()
		self.assertEqual(Drive.objects.all().count(), 0)
	
	# Verifies that when the end location is deleted,
	#  the associated drive is as well deleted
	def testEndLocationDeletion(self):
		Location.objects.get(location="End Location").delete()
		self.assertEqual(Drive.objects.all().count(), 0)
		
	# Verifies that when the dropoff location is deleted,
	#  the associated drive is not
	def testDropoffLocationDeletion(self):
		Location.objects.get(location="dropoff").delete()
		self.assertEqual(Drive.objects.all().count(), 1)
		
	# Verifies that when the driver user profile is deleted, the associated
	# drive is not deleted
	def testDriverDeletion(self):
		self.drive.driver.delete()
		self.assertEqual(Drive.objects.all().count(), 1)
		self.assertEqual(Location.objects.all().count(), 3)
		
	# Verifies that when the passenger is deleted, the associated
	# drive is not deleted
	def testPassengerDeletion(self):
		# Create a passenger and add them
		passenger = CustomUser.objects.create(username="Passenger")
		self.drive.add_passenger(passenger)
		
		self.drive.passengers.all().delete()
		self.assertEqual(Drive.objects.all().count(), 1)
		
	# Verifies that when the drive is deleted, the associated
	# user profiles are not deleted
	def testDriveDeletionOnUsers(self):
		# Create a passenger and add them
		passenger = CustomUser.objects.create(username="Passenger")
		self.drive.add_passenger(passenger)
		
		self.drive.delete()
		self.assertEqual(Drive.objects.all().count(), 0)
		self.assertEqual(CustomUser.objects.all().count(), 2)
		
	# Verifies the behavior of Drive.add_passenger
	# when num_passengers < max_passengers
	def testAddValidPassenger(self):
		passenger = CustomUser.objects.create(username="Passenger")
		result    = self.drive.add_passenger(passenger)
		
		self.assertEqual(result, True)
		self.assertEqual(self.drive.passengers.count(), 1)
	
	# Verifies the behavior of Drive.add_passenger
	# when num_passengers >= max_passengers
	def testAddInvalidPassenger(self):
		# Fill the car with passengers
		for i in range(self.drive.max_passengers):
			passenger = CustomUser.objects.create(username="Passenger" + str(i))
			self.drive.add_passenger(passenger)
			
		# Add one passenger too many
		passenger = CustomUser.objects.create(username="MaxPassenger")
		result    = self.drive.add_passenger(passenger)
		
		self.assertEqual(result, False)
		self.assertEqual(self.drive.passengers.count(), self.drive.max_passengers)
		
class DriveListingTester(TestCase):
	# Setup for all tests
	# Creates a sample drive with default values and none of the optional values
	def setUp(self):		
		self.start_location, self.end_location, self.driver, self.drive, self.dropoff = create_drive(
			"Name", start_location_str = "Start Location", end_location_str = "End Location", 
			title_str = "Drive Title", description_str = "Drive Description")
		self.start_location2, self.end_location2, self.driver2, self.drive2, self.dropoff2 = create_drive(
			"Name2", start_location_str = "Start Location2", end_location_str = "End Location2", 
			title_str = "Drive Title2", description_str = "Drive Description2")
		
	# Ensures that the create button brings us to the create drive page
	# TODO
	def testCreateButton(self):
		pass
		
	# Asserts that the default queryset returns all drives
	def testDefaultQuery(self):
		ridelist = RideList()
		queryset = ridelist.get_queryset()
		
		self.assertEqual(queryset.count(), 2)
		self.assertEqual(queryset[0].driver.username, "Name")
		self.assertEqual(queryset[1].driver.username, "Name2")

	def test_selenium(self):
		browser = get_chrome_driver()
		browser.get('https://duckduckgo.com')
		print(browser.page_source)