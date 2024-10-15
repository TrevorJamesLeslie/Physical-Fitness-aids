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

def spm_to_interval(spm):
    return 60 / spm

def beep_test(initial_spm=20, min_spm=20, max_spm=28, duration=60, sound_method='default'):
    print("Adjustable Rowing Beep Test")
    print("Press 'q' to quit, 'up' to increase SPM, 'down' to decrease SPM")
    print(f"Initial SPM: {initial_spm}")
    
    # Select beep function based on sound_method and platform
    if sound_method == 'playsound':
        beep = beep_playsound
    elif platform.system() == "Windows":
        beep = beep_winsound
    else:
        beep = beep_unix
    
    spm = initial_spm
    start_time = time.time()
    next_beep = start_time

    while time.time() - start_time < duration:
        current_time = time.time()
        interval = spm_to_interval(spm)
        
        if current_time >= next_beep:
            beep()
            next_beep = current_time + interval
            print(f"Beep! Current SPM: {spm:.1f} | Interval: {interval:.2f} seconds")

        if keyboard.is_pressed('q'):
            print("Test ended by user")
            break
        elif keyboard.is_pressed('up') and spm < max_spm:
            spm = min(spm + 0.5, max_spm)
            time.sleep(0.1)  # Prevent multiple rapid adjustments
        elif keyboard.is_pressed('down') and spm > min_spm:
            spm = max(spm - 0.5, min_spm)
            time.sleep(0.1)  # Prevent multiple rapid adjustments

    print("Test completed")

if __name__ == "__main__":
    # You can change 'default' to 'playsound' to use playsound instead of winsound/unix beep
    beep_test(sound_method='default')
