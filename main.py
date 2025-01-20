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

            time.sleep(0.1)  # Check for new files every 100ms
    except Exception as e:
        print(f"Error in monitoring: {e}")
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
    global exit_program
    try:
        while not exit_program:
            random_mouse_move()
            time.sleep(random_delay(2, 4))
            pyautogui.scroll(random.randint(-10, 10))
            if random.choice([True, False]):
                pyautogui.click(button=random.choice(['left', 'right']))
            pyautogui.press(random_key())
            time.sleep(random_delay(3, 10))
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

            while True:
                time.sleep(0.1)  # Keep the main thread alive for Ctrl+C
    except KeyboardInterrupt:
        print("\nProgram terminated with Ctrl+C. Goodbye!")
    except Exception as e:
        print(f"Unhandled error: {e}")
        print(104)
