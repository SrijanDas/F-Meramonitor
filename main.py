import pyautogui, sys, time, os, shutil
import requests
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 


MODIFIED_FILES = []

DESTINATION_PATH = '/home/srijan/MeraMonitor/Dezy It/srijan@dezyit.com/screenshots/'
SOURCE_PATH = "./images/"


# try:
#     while True:

#         # x, y = pyautogui.position()
#         # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         # print(positionStr, end='')
#         # print('\b' * len(positionStr), end='', flush=True)

#         # pyautogui.moveTo(100, 200, 2, pyautogui.easeInElastic)   # moves mouse to X of 100, Y of 200.
#         # time.sleep(5)
#         # pyautogui.click
#         # pyautogui.moveTo(None, 500, 2, pyautogui.easeOutQuad)  # moves mouse to X of 100, Y of 500.
#         # time.sleep(3)
#         # pyautogui.moveTo(600, None, 2, pyautogui.easeInOutQuad)
#         # time.sleep(3)
#         # pyautogui.scroll(10)
#         # time.sleep(1)
#         # pyautogui.click(button='left')
#         # time.sleep(2)
#         # pyautogui.press('capslock')
#         # time.sleep(10)  

# except KeyboardInterrupt:
#     print('\n')


def change_screenshot(file):
    print("Changing screenshot...")
    url = "https://api.apileague.com/retrieve-random-meme?keywords=dark&media-type=image"
    api_key = os.getenv('API_KEY')

    headers = {
        'x-api-key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        image_response = requests.get(data['url'], stream=True)

        if image_response.status_code == 200:
            # Save the image to a file
            file_to_remove = DESTINATION_PATH + file
            new_file = SOURCE_PATH + file
            print(new_file, file_to_remove)

            with open(new_file, 'wb') as file:
                for chunk in image_response.iter_content(1024):
                    file.write(chunk)
            print("Image successfully saved as" + new_file)

            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                shutil.copy2(new_file, file_to_remove)
                print("Screenshot changed successfully")
        else:
            print("Failed to retrieve the image. Status code:", image_response.status_code)

    else:
        print(f"Error: {response.status_code}\n")


def check_if_new_files():
    files = os.listdir(DESTINATION_PATH)
    new_files = []
    for f in files:
        if f.title().lower() not in MODIFIED_FILES:
            new_files.append(f.title().lower())
    return new_files


if __name__ == "__main__":
    try:
        while True:
            print("Checking for new files...")
            new_files = check_if_new_files()
            if len(new_files) == 0:
                # no new files
                print("no new files sleeping...\n")
                time.sleep(60)
            else:
                for i in range(len(new_files)):
                    if i % 2 == 0:
                        print(f"New file found: {new_files[i]}")
                        change_screenshot(new_files[i])
                        print("Modified files: \n", MODIFIED_FILES)
                        print("\n")

                    MODIFIED_FILES.append(new_files[i])

    except Exception as e:
        print(e)
