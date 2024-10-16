import subprocess
import sys
import importlib.util
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ['keyboard']
for package in required_packages:
    if importlib.util.find_spec(package) is None:
        print(f"{package} not found. Installing...")
        install(package)

import time
import keyboard
import winsound

class RowingBeepTest:
    def __init__(self, wav_file, initial_spm=20, min_spm=20, max_spm=28):
        self.wav_file = wav_file
        self.spm = initial_spm
        self.min_spm = min_spm
        self.max_spm = max_spm

    def play_beep(self):
        try:
            winsound.PlaySound(self.wav_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def adjust_spm(self, increment):
        self.spm = max(min(self.spm + increment, self.max_spm), self.min_spm)

    def get_interval(self):
        return 60 / self.spm

    def run_test(self, duration=60):
        print("Rowing Beep Test")
        print("Press 'q' to quit, 'up' to increase SPM, 'down' to decrease SPM")
        print(f"Initial SPM: {self.spm}")

        start_time = time.time()
        next_beep = start_time

        try:
            while time.time() - start_time < duration:
                current_time = time.time()
                
                if current_time >= next_beep:
                    self.play_beep()
                    next_beep = current_time + self.get_interval()
                    print(f"Beep! SPM: {self.spm} | Interval: {self.get_interval():.2f} s")

                if keyboard.is_pressed('q'):
                    print("Test ended by user")
                    break
                elif keyboard.is_pressed('up'):
                    self.adjust_spm(1)  # Changed to 1 for whole number increment
                    time.sleep(0.1)
                elif keyboard.is_pressed('down'):
                    self.adjust_spm(-1)  # Changed to -1 for whole number decrement
                    time.sleep(0.1)
        except Exception as e:
            print(f"An error occurred during the test: {e}")

        print("Test completed")

if __name__ == "__main__":
    try:
        wav_file = r"C:\Users\tonyl\Documents\GitHub\Physical-Fitness-aids\beep.wav"
        if not os.path.exists(wav_file):
            print(f"Error: WAV file not found at {wav_file}")
        else:
            test = RowingBeepTest(wav_file)
            test.run_test()
    except Exception as e:
        print(f"An error occurred: {e}")

input("Press Enter to exit...")
