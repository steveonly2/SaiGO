from lib.controls_module import *

def walk_to_vending_machine():
    keypress("a", 4200)
    keydown("a")
    keydown("w")
    sleep(6200)
    keyup("a")
    keyup("w")
    keypress("d", 500)

def open_vending_machine():
    keypress("s", 500)

def reset_from_vending_machine():
    keypress("w", 700)
    keypress("d", 3000)
    keydown("s")
    keydown("a")
    sleep(1200)
    jump()
    sleep(1000)
    keyup("s")
    sleep(600)
    jump()
    sleep(700)
    keyup("a")
    keydown("w")
    sleep(500)
    jump()
    sleep(300)
    keyup("w")

def buy_potion():
    if vending_machine_check() == True:
        move_to(40.52, 70)
        sleep(100)
        click()
        return True
    else:
        move_to(50, 70)
        sleep(100)
        click()
        return False

def vending_machine_check():
    screenshot(vending_machine_path, 40, 24.5, 20, 7.5)
    sleep(500)
    text = reader.readtext(vending_machine_path, detail=0)
    possible_detections = ["Hey", "Heey", "Heyl", "Hey!", "Heeyl", "Hley!", "Hley", "Hleey", "Hleeyl", "Hleey!"]
    for i in text:
        fail_counts = 0
        for v in possible_detections:
            if i == v:
                return True
            else:
                fail_counts += 1
        
        if fail_counts >= len(possible_detections):
            print("Vending Machine unavaliable.")
            return False

    print("Vending Machine not found.")
    return False