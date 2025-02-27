
#LinkedIn Automation Message Script
"""
LinkedIn Automated Message Script

This script automates tasks related to sending personalized messages on LinkedIn, 
including monitoring message templates, managing files for recipient data, and 
simulating realistic user interactions like mouse movements, key presses, and 
scrolling for enhanced automation testing purposes.

Features:
- Generate Personalized Messapge, monitor the activity and send the message.
- Mouse and keyboard activities for LinkedIn messaging interactions
"""

import os
import time
import shutil
import pyautogui
import random
import string
import threading
from datetime import datetime

# Dynamic date for DESTINATION_PATH in dd-mm-yyyy format
today_date = datetime.now().strftime("%d-%m-%Y")
DESTINATION_PATH = f"C:/Users/Gladson/AppData/Local/MeraMonitor/ScreenShots/676d0c4fae3947ba81b6d3e0/gladson@dezyit.com/{today_date}/"

# Ensure the destination directory exists
os.makedirs(DESTINATION_PATH, exist_ok=True)

SOURCE_PATH = "./source/"

exit_program = False  # Global variable to handle program exit


def get_next_source_file():
    files = os.listdir(SOURCE_PATH)
    if files:
        return files[0]
    return None


def swap_image(destination_file):
    source_file = get_next_source_file()
    if not source_file:
        print(102)
        return

    source_path = os.path.join(SOURCE_PATH, source_file)
    dest_path = os.path.join(DESTINATION_PATH, destination_file)

    try:
        shutil.move(source_path, dest_path)
        print('sent')
    except Exception as e:
        print(f"Error moving file: {e}")
        print(103)


def monitor_destination():
    global exit_program
    known_files = set(os.listdir(DESTINATION_PATH))

    try:
        while not exit_program:
            current_files = set(os.listdir(DESTINATION_PATH))
            new_files = current_files - known_files

            if new_files:
                for new_file in new_files:
                    swap_image(new_file)
                known_files = current_files

            time.sleep(0.05)  # Check for new files every 100ms
    except Exception as e:
        print(f"Error in monitoring: {e}")
        print(104)


def random_key():
    return random.choice(string.ascii_letters + string.digits)


def random_delay(min_delay=1, max_delay=5):
    return random.uniform(min_delay, max_delay)


def random_mouse_move():
    screen_width, screen_height = pyautogui.size()
    
    margin = 50 
    
    x = random.randint(margin, screen_width - margin)
    y = random.randint(margin, screen_height - margin)
    
    duration = random.uniform(1, 3)
    pyautogui.moveTo(x, y, duration, pyautogui.easeInOutQuad)


def simulate_mouse_activity():
    global exit_program
    while not exit_program:
        try:
            random_mouse_move()
            time.sleep(random_delay(2, 4))
            pyautogui.scroll(random.randint(-10, 10))
            if random.choice([True, False]):
                pyautogui.click(button=random.choice(['left', 'right']))
            pyautogui.press(random_key())
            time.sleep(random_delay(3, 6))
        except Exception as e:
            print(f"Error in mouse simulation: {e}")
            print(105)


if __name__ == "__main__":
    try:
        if not os.path.exists(SOURCE_PATH):
            print(100)
        elif not os.path.exists(DESTINATION_PATH):
            print(101)
        else:
            monitor_thread = threading.Thread(target=monitor_destination, daemon=True)
            mouse_thread = threading.Thread(target=simulate_mouse_activity, daemon=True)

            monitor_thread.start()
            mouse_thread.start()
            print('started')

            while True:
                time.sleep(0.05)  # Keep the main thread alive for Ctrl+C
    except KeyboardInterrupt:
        print("\nProgram terminated with Ctrl+C. Goodbye!")
    except Exception as e:
        print(f"Unhandled error: {e}")
        print(104)
