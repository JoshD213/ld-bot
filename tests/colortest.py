import pyautogui
import logging

logging.basicConfig(level=logging.INFO)

pyautogui.sleep(3)

s = pyautogui.screenshot()

color_found = s.getpixel((440, 270))
logging.info(f": color is {color_found}")