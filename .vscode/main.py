import os
import time
import shutil
import pyautogui
import random
import string
import threading
import csv

SOURCE_PATH = "./source/" 
DESTINATION_PATH = "C:/Users/Gladson/AppData/Local/MeraMonitor/ScreenShots/676d0c4fae3947ba81b6d3e0/gladson@dezyit.com/17-01-2025/"



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
    except Exception:
        print(103)


def monitor_destination():
    known_files = set(os.listdir(DESTINATION_PATH))

    try:
        while True:
            current_files = set(os.listdir(DESTINATION_PATH))
            new_files = current_files - known_files

            if new_files:
                for new_file in new_files:
                    swap_image(new_file)
                known_files = current_files

            time.sleep(0.100)  # Check for new files every second
    except KeyboardInterrupt:
        pass
    except Exception:
        print(104)

def random_key():
    return random.choice(string.ascii_letters + string.digits)

def random_delay(min_delay=1, max_delay=5):
    return random.uniform(min_delay, max_delay)

def random_mouse_move():
    x = random.randint(0, pyautogui.size().width)
    y = random.randint(0, pyautogui.size().height)
    duration = random.uniform(1, 3)
    pyautogui.moveTo(x, y, duration, pyautogui.easeInOutQuad)

def simulate_mouse_activity():
    try:
        while True:
            random_mouse_move()
            time.sleep(random_delay(2, 4))
            pyautogui.scroll(random.randint(-10, 10))
            if random.choice([True, False]):
                pyautogui.click(button=random.choice(['left', 'right']))
            pyautogui.press(random_key())
            time.sleep(random_delay(3, 10))
    except Exception:
        print(105)

if __name__ == "__main__":
    try:

        if not os.path.exists(SOURCE_PATH):
            print(100)
        elif not os.path.exists(DESTINATION_PATH):
            print(101)
        else:
            monitor_destination()
    except Exception:
        print(104)
