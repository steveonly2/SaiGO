import customtkinter, pyautogui, tkinter, os, sys, time, threading, keyboard, json, math, easyocr
from ahk import AHK
from PIL import Image

ahk = AHK()
reader = easyocr.Reader(['en'], gpu=True)

image_path = sys.path[0] + "\\images\\credits.png"
screenshot_path = sys.path[0] + "\\images\\screenshot.png"
vending_machine_path = sys.path[0] + "\\images\\vmp.png"
autoroll_path = sys.path[0] + "\\images\\autoroll.png"
temp_path = sys.path[0] + "\\images\\temp.png"
config_path = sys.path[0] + "\\config.json"

def get_xy(all = False):
    try:
        w = pyautogui.getWindowsWithTitle("Roblox")[0]
    except IndexError:
        print("No windows named 'Roblox' found.")
        return 0, 0

    width = w.width
    height = w.height
    padx = w.left
    pady = w.top

    if all == False:
        return width, height
    else:
        return width, height, padx, pady

def move_to(xp, yp): # Move to using percentage (take a screenshot of the whole screen and use GIMP to find the percentage)
    x, y = get_xy()
    xp = math.floor(0.01*x*xp)
    yp = math.floor(0.01*y*yp)
    ahk.mouse_move(xp, yp)

def click(b = "L", n = 1): # L R M | Left Right Middle
    ahk.click(button=b, click_count=n)

def mouse_hold(b = "L"):
    ahk.click(button=b, direction="Down")

def mouse_release(b = "L"):
    ahk.click(button=b, direction="Up")

def mouse_pos():
    x, y = ahk.mouse_position
    width, height = get_xy()
    xp = (x/width)*100
    yp = (y/height)*100
    return xp, yp

def focused_on_roblox():
    try:
        w = pyautogui.getWindowsWithTitle("Roblox")[0]
        w.activate()
        time.sleep(0.5)
    except IndexError:
        print("No windows named 'Roblox' found.")
        return IndexError

def sleep(l): # Sleeps in ms
    time.sleep(l/1000)

def press(k, l = 100):
    keyboard.press(k)
    time.sleep(l/1000)
    keyboard.release(k)

def getcolor(xp, yp):
    x, y = get_xy()
    xp = math.floor(0.01*x*xp)
    yp = math.floor(0.01*y*yp)
    return ahk.pixel_get_color(xp, yp)

def get_upgrade_startpos():
    move_to(1, 50)
    color_pos_list = ["0x777734", "0xF94900", "0xFFE900", "0xF9B300", "0xE396FF"]
    center = getcolor(50, 50)
    pos = 0

    for i in color_pos_list:
        pos +=1
        if center == i:
            return pos
    
    return 0

def go_to_startpos(n, c = False):
    startpos = get_upgrade_startpos()
    if startpos == 0:
        return 1
    elif startpos == n:
        return 2

    positions = [
        [0, (38.5, 55.3), (38.5, 43.5), (38.5, 37.7), (41.4, 35)],
        [(61.7, 43.3), 0, (50, 37.8), (50, 31.6), (52.8, 28.65)],
        [(61.5, 55.8), (50, 61.5), 0, (50, 43.8), (52.9, 41.2)],
        [(61.6, 61.9), (50, 68), (50, 55.5), 0, (52.9, 46.6)],
        [(58.9, 64.8), (47, 71), (47, 58.85), (47, 53.4), 0]
                 ]

    target = positions[startpos-1][n-1]

    move_to(target[0], target[1])

    if c == True:
        click()

def back_button_exists():
    pos = getcolor(55, 90)
    return True if pos == "0xFFFFFF" else False

def find_color(color, start1, start2, end1, end2):
    width, height = get_xy()
    try:
        x, y = ahk.pixel_search(color=color, search_region_start=(start1*width/100,start2*height/100), search_region_end=(end1*width/100,end2*height/100))
        xp = (x/width)*100
        yp = (y/height)*100
        return xp, yp
    except TypeError:
        return 0, 0

def keydown(key):
    ahk.key_down(key)

def keyup(key):
    ahk.key_up(key)

def keypress(key, duration = 100):
    if duration == 0:
        ahk.key_press(key)
    else:
        ahk.key_down(key)
        sleep(duration)
        ahk.key_up(key)

def jump():
    keypress("space")

def send(message):
    ahk.type(message)

def screenshot(path, x1 = 0, y1 = 0, x2 = 100, y2 = 100):
    width, height, padx, pady = get_xy(True)
    padxp = math.floor(padx/width*100)
    padyp = math.floor(pady/width*100)
    x1 = math.floor(width*x1/100) + padx
    x2 = math.floor(width*x2/100) + padxp
    y1 = math.floor(height*y1/100) + pady
    y2 = math.floor(height*y2/100) + padyp
    print(f"{x1}, {y1} | {x2}, {y2}")
    pyautogui.screenshot(path, region=(x1, y1, x2, y2))

def autoroll_check():
    screenshot(autoroll_path, 46.38, 93.14, 7.1, 5.4)
    sleep(500)
    text = reader.readtext(autoroll_path, detail=0)
    possible_detections = ["Roll!", "Rolll", "Roll", "Rol", "Ro!", "Ro!!"]
    for i in text:
        fail_counts = 0
        for v in possible_detections:
            if i == v:
                return False
            else:
                fail_counts += 1
                print(text)
        
        if fail_counts >= len(possible_detections):
            print("Autoroll already engaged!")
            return True

    print("Autoroll already engaged!")
    return True

def affordable_check():
    screenshot(temp_path, 44, 73.6, 11, 6)
    sleep(500)
    text = reader.readtext(temp_path, detail=0)
    print(text)
    possible_detections = ["Ok!", "Okl", "0k!", "0kl", "Ok", "0k", "OkI", "@k!", "@k", "@kI", "@kl", "@L"]
    for i in text:
        fail_counts = 0
        for v in possible_detections:
            if i == v:
                print("Not Affordable")
                return False
            else:
                fail_counts += 1
        
        if fail_counts >= len(possible_detections):
            print("Affordable")
            return True

    print("Affordable")
    return True