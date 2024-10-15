import subprocess
import sys
import importlib.util

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. You may need to install it manually.")
        sys.exit(1)

# Check and install required packages
required_packages = ['keyboard', 'playsound']
for package in required_packages:
    if importlib.util.find_spec(package) is None:
        print(f"{package} not found. Attempting to install...")
        install(package)

import time
import keyboard
import platform
import os

# Import sound modules
if platform.system() == "Windows":
    import winsound
from playsound import playsound

def beep_winsound():
    winsound.Beep(1000, 200)  # 1000 Hz for 200 ms

def beep_playsound():
    playsound('beep.wav', block=False)

def beep_unix():
    os.system("printf '\a'")  # Print the bell character

def calculate_spm(interval):
    return 60 / interval

def beep_test(initial_interval=3.00, final_interval=2.14, duration=60, sound_method='default'):
    print("Adjustable Beep Test for Rowing")
    print("Press 'q' to quit, 'up' to increase interval, 'down' to decrease interval")
    print(f"Initial interval: {initial_interval:.2f} seconds")
    
    # Select beep function based on sound_method and platform
    if sound_method == 'playsound':
        beep = beep_playsound
    elif platform.system() == "Windows":
        beep = beep_winsound
    else:
        beep = beep_unix
    
    interval = initial_interval
    start_time = time.time()
    next_beep = start_time

    while time.time() - start_time < duration:
        current_time = time.time()
        
        if current_time >= next_beep:
            beep()
            next_beep = current_time + interval
            spm = calculate_spm(interval)
            print(f"Beep! Current interval: {interval:.2f} seconds | Stroke Rate: {spm:.1f} SPM")

        if keyboard.is_pressed('q'):
            print("Test ended by user")
            break
        elif keyboard.is_pressed('up') and interval < 3.00:
            interval = min(interval + 0.01, 3.00)
            time.sleep(0.1)  # Prevent multiple rapid adjustments
        elif keyboard.is_pressed('down') and interval > 2.14:
            interval = max(interval - 0.01, 2.14)
            time.sleep(0.1)  # Prevent multiple rapid adjustments

    print("Test completed")

if __name__ == "__main__":
    # You can change 'default' to 'playsound' to use playsound instead of winsound/unix beep
    beep_test(sound_method='default')
