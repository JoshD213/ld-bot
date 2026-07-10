from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import time
import os
import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Run these AFTER the path fix
from level_timings import normalize_point

# Chrome
# chrome_options = ChromeOptions()
# driver = webdriver.Chrome(options=chrome_options)
# DOES NOT CLICK!

# Firefox
# profile_path = Path(__file__).parent / "FirefoxProfile"
# profile_path = profile_path.resolve()
# print(f"Profile path: {profile_path}")

# if not profile_path.is_dir():
#     raise FileNotFoundError(f"Firefox profile folder not found: {profile_path}")

firefox_options = FirefoxOptions()
# firefox_options.add_argument("-profile")
# firefox_options.add_argument(str(profile_path))

driver = webdriver.Firefox(options=firefox_options)

driver.get("https://poki.com/en/g/level-devil")
fs_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#fullscreen-button"))
)
fs_button.click()

time.sleep(10)
x, y = normalize_point(578, 668) # Working great for dynamic positioning
pyautogui.moveTo(x, y, duration=0.5)

pyautogui.click(x, y, clicks=2, interval=1)
# CLICKS WORKED! Requires first click to do nothing / make the window active

time.sleep(99999999)