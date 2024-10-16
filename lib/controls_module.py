import pyautogui, math, time, keyboard
from ahk import AHK

ahk = AHK()

def get_xy():
    try:
        w = pyautogui.getWindowsWithTitle("Roblox")[0]
    except IndexError:
        print("No windows named 'Roblox' found.")
        return 0, 0

    width = w.width
    height = w.height

    return width, height # x,y

def move_to(xp, yp): # Move to using percentage (take a screenshot of the whole screen and use GIMP to find the percentage)
    x, y = get_xy()
    xp = math.floor(0.01*x*xp)
    yp = math.floor(0.01*y*yp)
    ahk.mouse_move(xp, yp)

def click(b = "L", n = 1): # L R M | Left Right Middle
    ahk.click(button=b, click_count=n)

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
    move_to(1, 1)
    color_pos_list = ["0x777734", "0xF94900", "0xFFE900", "0xF9B300", "0xE396FF"]
    center = getcolor(50, 50)
    pos = 0

    for i in color_pos_list:
        pos +=1
        if center == i:
            return pos

def back_button():
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

def keypress(key, duration = 0):
    if duration == 0:
        ahk.key_press(key)
    else:
        ahk.key_down(key)
        sleep(duration)
        ahk.key_up(key)

def send(message):
    ahk.type(message)