# Delayed start
# every 5s, print the mouse x/y position to console logs
# after the 5s end, print a notification saying "move mouse to next position"

import pyautogui
import sys
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import connect_to_webdriver, send_notification

# boot up browser (optional)
driver = connect_to_webdriver()
driver.get("https://poki.com/en/g/level-devil")
send_notification("Clicking fullscreen", driver)
fs_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()

pyautogui.sleep(5)

while True:
    pyautogui.sleep(3)
    x, y = pyautogui.position()
    print(x, y)
    send_notification("MOVE!", driver)