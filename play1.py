from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import datetime
import time
import logging

# Absolute path of the directory
fileDir = os.path.dirname(os.path.abspath(__file__))

# Driver Configs
fileChromeDriver = os.path.join(fileDir, 'chromePath.txt')
so = open(fileChromeDriver)
chrome_path = so.read()
so.close()
logFile = "uploaderLog {}.log".format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
logging.basicConfig(filename=logFile, filemode='w',format='%(asctime)s-%(levelname)s - %(lineno)s  %(message)s', level=logging.INFO)
#chrome_path = "F:\\My Work\\python\\chromedriver.exe" # Chrome driver path
driver = None
delay = 30

# Login details
fileUsername = os.path.join(fileDir, 'username.txt')
bo = open(fileUsername)
username = bo.read()
bo.close()

filePassword = os.path.join(fileDir, 'password.txt')
bo2 = open(filePassword)
password = bo2.read()
bo2.close()

# Group ids
groups = ['1389919844566079','aiesecglobalexchange','176198385793293','149750071768943','425806367867419','195966297683683','709264009093812','563334607048707','1333468710000726','734676453227349','390010814385676','356961544333733','1077335595701483','333992393415198','2232632612']

# Post Settings
fileImage_src = os.path.join(fileDir, 'image_src.txt')
po = open(fileImage_src)
image = po.read()
po.close()
fileMassage = os.path.join(fileDir, 'massage.txt')
po2 = open(fileMassage)
massage = po2.read()
po2.close()

# Start chrome with options (Options : Disable notifications)
def startChrome():
	global driver
	try:
		options = webdriver.ChromeOptions() 
		prefs = {"profile.default_content_setting_values.notifications" : 2} # Chrome option to disable notification popup
		options.add_experimental_option("prefs",prefs)
		driver = webdriver.Chrome(chrome_path, options=options)
		driver.get("https://facebook.com")
		logging.info("STARTING CHROME SUCCESSFUL")
	except:
		logging.critical("STARTING CHROME ERROR", exc_info=True)

# Login to account
def login(username, password):
	try:
		driver.find_element_by_name("email").send_keys(username)
		driver.find_element_by_name("pass").send_keys(password + "\n")
		logging.info("LOGIN SUCCESSFUL")
	except:
		logging.critical("LOGIN ERROR", exc_info=True)

# Upload image
def upload_photo(image):
	try:
		try:
			WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bp9cbjyn.j83agx80.taijpn5t.dfwzkoeu.ni8dbmo4.stjgntxs')))
		except TimeoutException:
			logging.critical('Loading took too much time! - @getting_go_back_link')
		driver.find_elements_by_css_selector("input[type=file]")[0].send_keys(image)
		logging.info("IMAGE UPLOAD SUCCESSFUL")
	except:
		logging.critical("IMAGE UPLOAD ERROR", exc_info=True)

# Input text of the post
def input_text(text):
	try:
		textContainer = driver.find_elements_by_css_selector("._1mf._1mj")[1]
		action = ActionChains(driver)
		action.click(textContainer)
		action.send_keys(text)
		action.perform()
		logging.info("TEXT ENTERING SUCCESSFUL")
	except:
		logging.critical("TEXT ENTERING ERROR", exc_info=True)

# Make the post
def make_post(image, text):
	upload_photo(image)
	time.sleep(3)
	input_text(text)

# Publish the post
def publish_post():
	try:
		toPost = driver.find_element_by_xpath("//span[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5' and text()='Post']")
		toPost.click()
		logging.info("POSTING SUCCESSFUL")
	except:
		logging.critical("POSTING ERROR", exc_info=True)

# Opens a new tab and focuses on that
def newTab():
	try:
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[-1])
		logging.info("NEW TAB OPENNING SUCCESSFUL")
	except:
		logging.critical("NEW TAB OPENNING ERROR", exc_info=True)

startChrome()
login(username, password)
for grp in groups:
	newTab()
	driver.get("https://facebook.com/" + grp)
	make_post(image, massage)
	publish_post()