from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from drives.models import *
from users.models import CustomUser
from django.utils import timezone
from drives.views import *
import RideOn.SeleniumTester as selenium_tester
from django.test.utils import override_settings

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
		
@override_settings(DEBUG=True)
class DriveListingTester(StaticLiveServerTestCase):
	# Setup for all tests
	# Creates a sample drive with default values and none of the optional values
	def setUp(self):		
		self.start_location, self.end_location, self.driver, self.drive, self.dropoff = create_drive(
			"Name", start_location_str = "Start Location", end_location_str = "End Location", 
			title_str = "Drive Title", description_str = "Drive Description")
		self.start_location2, self.end_location2, self.driver2, self.drive2, self.dropoff2 = create_drive(
			"Name2", start_location_str = "Start Location2", end_location_str = "End Location2", 
			title_str = "Drive Title2", description_str = "Drive Description2")
			
		self.browser = selenium_tester.create_chrome_driver()
		
	def tearDown(self):
		self.browser.close()
		
	# Ensures that the create button brings us to the create drive page
	def testCreateButton(self):
		self.browser.get(self.live_server_url + '/drives/')
		
		create_button = self.browser.find_element_by_id('create_drive')
		create_button.click()

		self.assertEqual(self.browser.current_url, self.live_server_url + '/drives/new')
		
	# Asserts that the default queryset returns all drives
	def testDefaultQuery(self):
		ridelist = RideList()
		queryset = ridelist.get_queryset()
		
		self.assertEqual(queryset.count(), 2)
		self.assertEqual(queryset[0].driver.username, "Name")
		self.assertEqual(queryset[1].driver.username, "Name2")
		
'''
Used to test the passenger sub-system from a GUI perspective.
Verifies underlying models as well.
Does not test API endpoints.
'''
@override_settings(DEBUG=True)
class PassengerSystemGUITester(StaticLiveServerTestCase):
		
	# Setup for all tests
	# Creates a sample drive with default values and none of the optional values
	def setUp(self):		
		self.start_location, self.end_location, self.driver, self.drive, self.dropoff = create_drive(
			"Name", start_location_str = "Start Location", end_location_str = "End Location", 
			title_str = "Drive Title", description_str = "Drive Description")
		self.start_location2, self.end_location2, self.driver2, self.drive2, self.dropoff2 = create_drive(
			"Name2", start_location_str = "Start Location2", end_location_str = "End Location2", 
			title_str = "Drive Title2", description_str = "Drive Description2")
			
		self.browser = selenium_tester.create_chrome_driver()
		
	def tearDown(self):
		self.browser.close()
		
	####################################
	# Test the join ride functionality #
	####################################
	
	# Ensures that when looking at a drive you do not own or are 
	# a part of that there is a button asking to join the ride
	def testJoinRideButtonExists(self):
		# View the drive as an unaffiliated user
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)
		
		join_btn = self.browser.find_element_by_id('join_ride_btn')
		self.assertEqual(join_btn.text, "Join Ride")
		
	# Ensures that clicking the 'Join Ride' button  
	# the user gets added to the ride waitlist
	def testJoinRideButtonWorks(self):
		# View the drive as an unaffiliated user
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)
		
		# Click 'Join Ride'
		join_btn = self.browser.find_element_by_id('join_ride_btn')
		join_btn.click()
		
		# Verify that user1 is now on the request list		
		self.assertEqual(self.drive2.requestList.all().get(id=self.driver.id).username, self.driver.username)
		
	# Ensures that if a user is on the request list of a ride
	# there is a message that tells them this
	def testWaitlistMessage(self):
		# Have user1 join ride2's requestlist
		self.drive2.requestList.add(self.driver)
		
		# View the drive as user1
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)
		
		# Verify that there's a message about being on the waitlist	
		waitlist_message = self.browser.find_element_by_id('waitlist_message')
		self.assertEqual(waitlist_message.text, "You're on the waitlist!")
	
	# Ensures that the owner can see requests to join a drive
	def testRequestAppears(self):
		# Have user1 join ride2's requestlist
		self.drive2.requestList.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Ensure user1's request is visible
		request_entry = self.browser.find_element_by_id('passenger_request')
		self.assertEqual(request_entry.text, self.driver.username)
		
	# Ensures that the non-owners can't see requests to join a drive
	def testRequestDoesntAppear(self):
		# Have user1 join ride2's requestlist
		self.drive2.requestList.add(self.driver)
		
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)

		# Ensure user1's request is not visible
		request_entry = selenium_tester.safe_find_element_by_id(self.browser, 'passenger_request')
		self.assertEqual(request_entry, None)
		
	# Ensures that the button to reject waitlist request works
	def testRejectRequestBtnWorks(self):
		# Have user1 join ride2's requestlist
		self.drive2.requestList.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Reject the request
		reject_button = self.browser.find_element_by_id('reject_request_btn')
		reject_button.click()
		
		# Ensure user1 is no longer on the waitlist
		self.assertEqual(self.drive2.requestList.count(), 0)
		
	# Ensures that the button to accept waitlist request works
	def testAcceptRequestBtnWorks(self):
		# Have user1 join ride2's requestlist
		self.drive2.requestList.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Reject the request
		accept_button = self.browser.find_element_by_id('accept_request_btn')
		accept_button.click()
		
		# Ensure user1 is no longer on the waitlist
		self.assertEqual(self.drive2.requestList.count(), 0)
		
		# Ensure user1 is on the passenger list
		self.assertEqual(self.drive2.passengers.filter(id=self.driver.id).count(), 1)
		
	# Ensures that owners can see passengers of a drive
	def testRequestAppearsOwner(self):
		# Have user1 join ride2 as a passenger
		self.drive2.passengers.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Ensure user1 shows in the passenger table
		passenger_entry = self.browser.find_element_by_id("passenger_entry")
		self.assertEqual(passenger_entry.text, self.driver.username)
		
	# Ensures that non-owners can see passengers of a drive
	def testRequestAppearsNonOwner(self):
		# Have user1 join ride2 as a passenger
		self.drive2.passengers.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)

		# Ensure user1 shows in the passenger table
		passenger_entry = self.browser.find_element_by_id("passenger_entry")
		self.assertEqual(passenger_entry.text, self.driver.username)
		
	# Ensures that the button to remove someone from a drive works
	def testRemovePassengerBtnWorks(self):
		# Have user1 join ride2's requestlist
		self.drive2.passengers.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Remove the passenger
		remove_button = self.browser.find_element_by_id('passenger_remove_btn')
		remove_button.click()
		
		# Ensure user1 is no longer a passenger
		self.assertEqual(self.drive2.passengers.count(), 0)
		
	# Ensures that the button to remove someone from a drive doesn't
	# appear for non-owners
	def testRemovePassengerBtnInvisible(self):
		# Have user1 join ride2 as a passenger
		self.drive2.passengers.add(self.driver)
		
		# View the ride as a non-owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)

		# Ensure the remove button doesn't exist
		remove_button = selenium_tester.safe_find_element_by_id(self.browser, 'passenger_remove_btn')
		self.assertEqual(remove_button, None)
		
	# Ensures that the button to leave a drive shows up for the passenger
	def testRemovePassengerBtnWorks(self):
		# Have user1 join ride2 as a passenger
		self.drive2.passengers.add(self.driver)
		
		# View the ride as the passenger
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver)

		# Remove the passenger
		leave_button = self.browser.find_element_by_id('leave_ride_btn')
		leave_button.click()
		
		# Ensure user1 is no longer a passenger
		self.assertEqual(self.drive2.passengers.count(), 0)
		
	# Ensures that the button to leave a drive doesn't
	# appear for anyone except that one passenger
	def testRemovePassengerBtnInvisible(self):
		user3 = CustomUser.objects.create(username="user3")
		
		# Have user1 join ride2 as a passenger
		self.drive2.passengers.add(self.driver)
		
		# View the ride as the owner
		self.browser.delete_all_cookies()
		self.browser.get(self.live_server_url + '/drives/' + str(self.drive2.id))
		selenium_tester.login_as(self.browser, self.driver2)

		# Ensure the leave button doesn't exist
		leave_button = selenium_tester.safe_find_element_by_id(self.browser, 'leave_ride_btn')
		self.assertEqual(leave_button, None)
		
		# View the ride as user3
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, user3)

		# Ensure the leave button doesn't exist
		leave_button = selenium_tester.safe_find_element_by_id(self.browser, 'leave_ride_btn')
		self.assertEqual(leave_button, None)