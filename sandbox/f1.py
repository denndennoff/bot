import slack
import os
import io
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from PIL import Image

options = Options()
options.headless = True
#options.add_argument('--headless')

driver = webdriver.Firefox(options=options, executable_path=r'E:/geckodriver-v0.24.0-win64/geckodriver.exe')
driver.get('https://gbtecag.atlassian.net')

email = driver.find_element_by_css_selector('#username')
email.send_keys(os.environ['JIRA_EMAIL'])

button_continue = driver.find_element_by_css_selector('#login-submit > span > span')
button_continue.click()

wait_for_password_field = WebDriverWait(driver, 15).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#password')))

password = driver.find_element_by_css_selector('#password')
password.send_keys(os.environ['JIRA_PASSWORD'])

button_login = driver.find_element_by_css_selector('#login-submit')
button_login.click()

time.sleep(15)

chart = driver.find_element_by_xpath('//*[@id="gadget-10694-chrome"]')
byte_chart_image = chart.screenshot_as_png
byte_chart_image = Image.open(io.BytesIO(byte_chart_image))
chart_image = byte_chart_image.save('chart.png')


client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

response = client.files_upload(
    channels="CLFU3LFFY",
    file="chart.png",
    filename='burndown_chart_sirius',
    initial_comment='Hello team! Here is our burndown chart! Enjoy it! :slightly_smiling_face:'
)
assert response["ok"]
