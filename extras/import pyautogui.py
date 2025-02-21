import pyautogui
import keyboard
import time
import threading

# Global flag to track whether clicking should continue
clicking = False

def click_mouse():
    global clicking
    while True:
        if clicking:
            pyautogui.click()  # Perform a click
            time.sleep(0.02)  # Wait for 1/50th of a second (~50 clicks per second)

def toggle_clicking():
    global clicking
    while True:
        if keyboard.is_pressed('t'):  # Check if 'T' key is pressed
            clicking = not clicking  # Toggle clicking state
            time.sleep(0.5)  # Add a delay to prevent multiple toggles from a single press

# Start the click thread
click_thread = threading.Thread(target=click_mouse)
click_thread.daemon = True  # Make sure the thread ends when the main program ends
click_thread.start()

# Start the toggle thread to listen for 'T' key press
toggle_thread = threading.Thread(target=toggle_clicking)
toggle_thread.daemon = True
toggle_thread.start()

# Keep the program running
while True:
    time.sleep(1)
