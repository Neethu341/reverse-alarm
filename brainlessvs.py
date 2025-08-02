import time
import datetime
import ctypes
import pygame
import threading
import tkinter as tk

# --- Alarm Settings ---
ALARM_HOUR = 7
ALARM_MINUTE = 30

# --- Idle Detection (Windows) ---
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

# --- Alarm Logic ---
def current_time():
    return datetime.datetime.now()

def is_before_alarm():
    now = current_time()
    alarm_time = now.replace(hour=ALARM_HOUR, minute=ALARM_MINUTE, second=0, microsecond=0)
    return now < alarm_time

def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")  # Ensure this file exists in the same folder
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# --- Reverse Alarm Monitoring ---
def monitor_activity(status_label):
    status_label.config(text="Monitoring... Move to trigger alarm")

    def check_loop():
        while True:
            idle = get_idle_time()
            if idle < 1:
                status_label.config(text="Activity detected — playing alarm!")
                play_alarm()
                break
            time.sleep(1)

    threading.Thread(target=check_loop).start()

# --- GUI Setup ---
def create_gui():
    window = tk.Tk()
    window.title("Reverse Alarm (Auto Start)")
    window.geometry("400x150")

    tk.Label(window, text="Reverse Alarm Clock", font=("Arial", 18)).pack(pady=10)
    tk.Label(window, text=f"Alarm Time: {ALARM_HOUR:02d}:{ALARM_MINUTE:02d}").pack()

    status_label = tk.Label(window, text="Starting...", fg="blue", font=("Arial", 12))
    status_label.pack(pady=10)

    if is_before_alarm():
        monitor_activity(status_label)
    else:
        status_label.config(text="It's already after the alarm time.")

    window.mainloop()

# --- Run the App ---
if __name__ == "__main__":
    create_gui()


