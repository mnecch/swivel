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
    if orientation == ds.DisplayOrientation:
        return
    ds.PelsHeight, ds.PelsWidth = ds.PelsWidth, ds.PelsHeight
    ds.DisplayOrientation = not ds.DisplayOrientation
    win32api.ChangeDisplaySettingsEx(DISPLAY_NAME, ds)

ard = serial.Serial(ARDUINO_PORT)
while True:
    ard.flushInput()
    try:
        ard_bytes = ard.readline()
        y = float(ard_bytes.decode("utf-8"))
        if y > 0.5:
            orient_display(LANDSCAPE)
        else:
            orient_display(PORTRAIT)
    except:
        break
    time.sleep(SLEEP_TIME)
