from selenium import webdriver
import os

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

# Create the chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")
chrome_options.headless = headless

# Set binary location if on Windows
if os.name == 'nt':
	chrome_options.binary_location = chrome_path + "chrome.exe"

chrome_driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
		
def get_chrome_driver():
	return chrome_driver