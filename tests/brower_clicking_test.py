from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import time
from level_timings import normalize_point

# Chrome
# chrome_options = ChromeOptions()
# driver = webdriver.Chrome(options=chrome_options)
# DOES NOT CLICK!

# Firefox
firefox_options = FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)
# CLICKS WORKED! Requires first click to do nothing / make the window active

driver.get("https://poki.com/en/g/level-devil")
fs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()

time.sleep(10)
x, y = normalize_point(578, 668) # Working great for dynamic positioning
pyautogui.moveTo(x, y, duration=0.5)
pyautogui.click()
time.sleep(1)
pyautogui.click()
time.sleep(1)
pyautogui.click()
time.sleep(1)
pyautogui.click()
time.sleep(10)