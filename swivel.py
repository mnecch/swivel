import time

import serial
import win32api

ARDUINO_PORT = 'COM6'
DISPLAY_NUM = 1
SLEEP_TIME = 15

LANDSCAPE = 0
PORTRAIT = 1

DISPLAY_NAME = win32api.EnumDisplayDevices(None, DISPLAY_NUM).DeviceName

def orient_display(orientation):
    ds = win32api.EnumDisplaySettings(DISPLAY_NAME, -1)
    ds.PelsHeight, ds.PelsWidth = ds.PelsWidth, ds.PelsHeight
    ds.DisplayOrientation = not ds.DisplayOrientation
    win32api.ChangeDisplaySettingsEx(DISPLAY_NAME, ds)
    return ds.DisplayOrientation

ard = serial.Serial(ARDUINO_PORT)
current_orientation = win32api.EnumDisplaySettings(DISPLAY_NAME, -1).DisplayOrientation
while True:
    ard.flushInput()
    try:
        ard_bytes = ard.readline()
        y = float(ard_bytes.decode("utf-8"))
        if y > 0.5 and current_orientation != LANDSCAPE:
            current_orientation = orient_display(LANDSCAPE)
        elif y <= 0.5 and current_orientation != PORTRAIT:
            current_orientation = orient_display(PORTRAIT)
    except:
        break
    time.sleep(SLEEP_TIME)
