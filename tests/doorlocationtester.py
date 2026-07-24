import pyautogui
import logging
from colorist import ColorRGB
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from level_timings import door_positions
from utils import send_notification, connect_to_webdriver

logging.basicConfig(level=logging.INFO)

# boot up browser (optional)
driver = connect_to_webdriver()
driver.get("https://poki.com/en/g/level-devil")
send_notification("Clicking fullscreen", driver)
fs_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()

logging.info("move to browser")
pyautogui.sleep(5)

logging.info("moving mouse out of the way before screenshotting")
pyautogui.moveTo(10, 10)

s = pyautogui.screenshot()
screenshot_size = s.size
screen_size = pyautogui.size()
retina_display = (screen_size != screenshot_size)

logging.info(f"{s.mode}, {s.size}, {s.format}")
logging.info(f"{pyautogui.size()}")

logging.info("move to cordinate")
for door, position in door_positions.items():
    x, y = position
    
    if retina_display:
        logging.info("Retina display!")
        x = x * 2
        y = y * 2

    r, g, b = s.getpixel((x, y))
    logging.info(f"{ColorRGB(r,g,b)}{door} {x, y}: color is this {r},{g},{b}{ColorRGB(r,g,b).OFF}")


for position in door_positions.values():
    pyautogui.moveTo(position)
    pyautogui.sleep(0.5)
