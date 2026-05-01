import pyautogui
from utils import connect_to_webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from level_timings import normalize_point


driver = connect_to_webdriver()
driver.get("https://poki.com/en/g/level-devil")
fs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()

time.sleep(5)
x, y = normalize_point(578, 668)

pyautogui.moveTo(x, y, duration=0.5)
a = pyautogui.click()
print(a)
a = pyautogui.leftClick()
print(a)