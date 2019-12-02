from django.test import Client, TestCase
from django.contrib.auth import authenticate
from users.models import CustomUser
from users.forms import CustomUserChangeForm
from users.custom_social_auth_pipeline import allowed_email 
from django.test.utils import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from drives.models import *
import RideOn.SeleniumTester as selenium_tester

class UserTester(TestCase):
    """
    Social auth tests.
    """
    def setUp(self):
        pass

    def testCreateValidNewUser(self):
        self.user = CustomUser.objects.create_user(username='hacker@virginia.edu', email='hacker@virginia.edu', password='12345')
        self.user.set_password('12345')
        self.user.save()
        self.assertEqual(CustomUser.objects.all().count(), 1)
        
    def testCreateUserInvalidEmail(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.assertFalse(allowed_email(self.user.email))
    
    def testUserLogin(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.user.set_password('12345')
        self.user.save()
        
        authenticated_user = authenticate(username='testuser', password='12345')
		
        self.assertEqual(self.user, authenticated_user)

class UserEditsTester(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='hacker@virginia.edu', email='hacker@virginia.edu', password='12345')

    def testFormEditAllFieldsValid(self):
        form = CustomUserChangeForm(data={'username':'John_Doe' , 'gender':'Male', 'phone':'+17037561234', 'about':'Some About'})
        self.assertTrue(form.is_valid())

    def testFormEditInvalidPhone(self):
        form = CustomUserChangeForm(data={'username':'John_Doe' , 'gender':'Male', 'phone':'+1703756123w', 'about':'Some About'})
        self.assertFalse(form.is_valid())

    def testProfileEditAllFieldsValid(self):
        local_fields = ['username', 'gender', 'phone', 'about']
        correct_data = {'username':'striker417' , 'gender':'Male', 'phone':'+17037561234', 'about':'I am a god at soccer'}
        self.form = CustomUserChangeForm(data={'username':'striker417' , 'gender':'Male', 'phone':'+17037561234', 'about':'I am a god at soccer'}, instance=self.user)
        if self.form.is_valid():
            self.form.save()

        for field in local_fields:
            self.assertTrue(getattr(self.user, field, '') == correct_data[field] )
			
'''
Used to test the review sub-system from a GUI perspective.
Verifies underlying models as well.
Does not test API endpoints.
'''
@override_settings(DEBUG=True)
class UserTestReviews(StaticLiveServerTestCase):
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
		self.browser.get(self.live_server_url)
		
	def tearDown(self):
		self.browser.close()
		
	# Ensures driver review exists when drive is completed
	def testDriverReviewExists(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver2)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id) + '/myrides/')
		
		# Verify that the review driver button exists
		driver_review = self.browser.find_element_by_id("driverReviewBtn")
		self.assertEqual(driver_review.text, "Review " + self.driver.username)
	
	# Ensures driver review does not exist for driver
	def testDriverReviewNotExist(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as driver and go to reviews
		# View the ride as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id) + '/myrides/')
		
		# Verify that the review driver button exists
		driver_review = selenium_tester.safe_find_element_by_id(self.browser, "driverReviewBtn")
		self.assertEqual(driver_review, None)
		
	# Ensures passenger review exists when drive is completed
	def testPassengerReviewExists(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id) + '/myrides/')
		
		# Verify that the review driver button exists
		passenger_review = self.browser.find_element_by_id("passengerReviewBtn")
		self.assertEqual(passenger_review.text, "Review " + self.driver2.username)
	
	# Ensures passenger review does not exist for passenger
	def testPassengerReviewNotExist(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as driver and go to reviews
		# View the ride as passenger
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver2)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id) + '/myrides/')
		
		# Verify that the review driver button exists
		passenger_review = selenium_tester.safe_find_element_by_id(self.browser, "passengerReviewBtn")
		self.assertEqual(passenger_review, None)	
		
		
	def submitReview(self):
		# Sleep to make sure the modal loads properly
		import time
		time.sleep(3)
		
		title = self.browser.find_element_by_id("reviewTitle")
		title.send_keys("Test Title")
		
		rating = self.browser.find_element_by_id("reviewRating")
		rating.send_keys("4")
		
		description = self.browser.find_element_by_id("reviewDescription")
		description.send_keys("Test Description")
	
		submit = self.browser.find_element_by_id("reviewSubmitBtn")
		submit.click()
		
		# Sleep to make sure the modal loads properly
		import time
		time.sleep(3)
	
	# Ensures driver review submission works
	def testDriverReviewSubmits(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver2)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id) + '/myrides/')
		
		# Submit a review
		driver_review = self.browser.find_element_by_id("driverReviewBtn")
		driver_review.click()
		self.submitReview()
		
	# Ensures passenger review submission works
	def testPassengerReviewSubmits(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id) + '/myrides/')
		
		# Submit a review
		passenger_review = self.browser.find_element_by_id("passengerReviewBtn")
		passenger_review.click()
		self.submitReview()	
		
	# Asserts that after the review is submitted
	# the button to submit no longer shows
	def testPassengerReviewGone(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id) + '/myrides/')
		
		# Submit a review
		passenger_review = self.browser.find_element_by_id("passengerReviewBtn")
		passenger_review.click()
		self.submitReview()
		
		# Assert that the submit button is gone
		passenger_review = selenium_tester.safe_find_element_by_id(self.browser, "passengerReviewBtn")
		self.assertEqual(passenger_review, None)	
		
	# Asserts that after the review is submitted
	# the button to submit no longer shows
	def testDriverReviewGone(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver2)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id) + '/myrides/')
		
		# Submit a review
		driver_review = self.browser.find_element_by_id("driverReviewBtn")
		driver_review.click()
		self.submitReview()
		
		# Assert that the submit button is gone
		driver_review = selenium_tester.safe_find_element_by_id(self.browser, "driverReviewBtn")
		self.assertEqual(driver_review, None)
		
	# Asserts that the driver rating changes after a review
	# is submitted
	def testDriverRatingChanges(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver2)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id) + '/myrides/')
		
		# Submit a review
		driver_review = self.browser.find_element_by_id("driverReviewBtn")
		driver_review.click()
		self.submitReview()
		
		# View the rating
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id))
		rating = self.browser.find_element_by_id("driverRating")
		
		self.assertEqual(rating.text.strip(), "4.00")
		
	def testPassengerRatingChanges(self):
		# Add passenger and complete drive
		self.drive.add_passenger(self.driver2)
		Drive.objects.filter(id=self.drive.id).update(status="Completed")
		
		# Login as passenger and go to reviews
		# View the ride not as the owner
		self.browser.delete_all_cookies()
		selenium_tester.login_as(self.browser, self.driver)
		self.browser.get(self.live_server_url + '/users/' + str(self.driver.id) + '/myrides/')
		
		# Submit a review
		passenger_review = self.browser.find_element_by_id("passengerReviewBtn")
		passenger_review.click()
		self.submitReview()
		
		# View the rating
		self.browser.get(self.live_server_url + '/users/' + str(self.driver2.id))
		rating = self.browser.find_element_by_id("riderRating")
		
		self.assertEqual(rating.text.strip(), "4.00")
		
	