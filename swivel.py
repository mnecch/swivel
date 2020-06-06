import time

import serial
import win32api

ARDUINO_PORT = 'COM6'
DISPLAY_NUM = 1
SLEEP_TIME = 15

LANDSCAPE = 0
PORTRAIT = 1

def orient_display(orientation):
    dd = win32api.EnumDisplayDevices(None, DISPLAY_NUM)
    dds = win32api.EnumDisplaySettings(dd.DeviceName, -1)
    if orientation == dds.DisplayOrientation:
        return
    dds.PelsHeight, dds.PelsWidth =  dds.PelsWidth, dds.PelsHeight
    dds.DisplayOrientation = not dds.DisplayOrientation
    win32api.ChangeDisplaySettingsEx(dd.DeviceName, dds)


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
