from selenium import webdriver
import os
from django.test import Client 

# Extract settings from path variables or use default values
chrome_path = os.getenv('CHROME_PATH')
driver_path = os.getenv('DRIVER_PATH')
headless    = os.getenv('HEADLESS')
if not chrome_path:
	chrome_path = "D:/Program Files (x86)/Google/Chrome/Application/"
if not driver_path:
	if os.name == 'nt':
		driver_path = chrome_path + "chromedriver.exe"
	else:
		driver_path = "/usr/bin/chromedriver"
if headless == "True":
	headless = True
else:
	headless = False
		
# Print settings for debug purposes
print("Settings:")
print("chrome path: " + chrome_path)
print("driver path: " + driver_path)
print("headless: " + str(headless))
		
def create_chrome_driver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument("--test-type")
	chrome_options.add_argument("--log-level=3")
	chrome_options.headless = headless

	# Set binary location if on Windows
	if os.name == 'nt':
		chrome_options.binary_location = chrome_path + "chrome.exe"

	return webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
	
def login_as(browser, user):
	client = Client()
	client.force_login(user)
	sessionid_cookie = client.cookies.get("sessionid").output(attrs=["sessionid"], header='').strip()
	sessionid = sessionid_cookie.split("=")[1]
	
	browser.add_cookie({'name': 'sessionid', 'value': sessionid})
	browser.refresh()
	
def safe_find_element_by_id(browser, id):
	try:
		return browser.find_element_by_id(id)
	except:
		return None