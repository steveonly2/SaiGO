import customtkinter, pyautogui, tkinter, os, sys, time, threading, keyboard, json, math
from ahk import AHK
from PIL import Image

from lib.controls_module import * # modules in /lib

ahk = AHK()

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
app = customtkinter.CTk()
app.title("SaiGO")
app.geometry("300x300")

tabView = customtkinter.CTkTabview(app)
tabView.pack(padx=20, pady=20)
tabView.add("Main")
tabView.add("Settings")
tabView.add("Credits")

default_settings = {
    "is_running": 0,
    "darkmode": 0,
    "autoclicker": 0,
    "autoclicker_running": 0,
    "upgrade": 0,
    "upgrade_delay": 5,
    "upgrade_startpos": 0,
    "upgrade_cooldown": 0
    }


# -------- CONFIGS -------- #


config_path = os.path.join(sys.path[0], 'config.json')

if not os.path.isfile(config_path):
    with open(config_path, 'w') as f:
        json.dump(default_settings, f)
        
with open(config_path, 'r') as f:
    config = json.load(f)

for key in default_settings.keys():
    if key in config:
        default_settings[key] = config[key]

    with open(config_path, 'w') as f:
        json.dump(default_settings, f)

    config = default_settings

if config["darkmode"] == 1:
    customtkinter.set_appearance_mode('dark')

def update_config():
    with open(config_path, 'w') as f:
        json.dump(config, f)


# -------- MAIN LOOPS -------- #


def mainLoop():
    while config["is_running"] == 1:

        if config["upgrade"] == 1:
            if config["upgrade_cooldown"] == 0:

                config["upgrade_cooldown"] = config["upgrade_delay"]*60
                update_config()
                enter_upgrade()
                sleep(1000)
                startpos = get_upgrade_startpos()
                print(startpos)
                sleep(1000)

                if startpos == 1:
                    move_to(50, 50)
                    sleep(500)
                    click()
                    sleep(1000)
                    back_upgrade()
                    exit_upgrade()

        if config["autoclicker"] == 1:
            config["autoclicker_running"] = 1
            update_config()

            while config["upgrade_cooldown"] != 0 or config["upgrade"] != 1:
                click_loop()

            sleep(1500)
                
def secLoop():
    while config["is_running"] == 1:

        if config["upgrade_cooldown"] == 0 and config["upgrade"] == 1:
            config["autoclicker_running"] = 0
            update_config()

        if config["upgrade"] == 1:
            while config["upgrade_cooldown"] != 0:
                sleep(1000)
                config["upgrade_cooldown"] -= 1
                update_config()

            sleep(1000)


# -------- AUTOMATIONS -------- #


def click_loop():
    if config["autoclicker"] == 1:
        while config["autoclicker_running"] == 1:
            if mouse_pos() != (50, 87.5):
                move_to(50, 87.5) # Move to the specified coordinates
            try:
                click()  # Click
                sleep(75)  # Small delay between clicks
            except OverflowError:
                print("Overflow error in clicking")
                break  # Exit the loop if there's an error

def begin_macro():
    try:
        focused_on_roblox()
    except IndexError:
        end_macro()
        sleep(2000)

    config["is_running"] = 1  # Set the control variable to True
    update_config()

    enter_upgrade()
    reset_upgrade_zoom()
    if back_button() == True:
        back_upgrade()
    exit_upgrade()

    print("Auto Click Macro started")
        
    # Start the clicking loop in a new thread
    threading.Thread(target=mainLoop, daemon=True).start()
    threading.Thread(target=secLoop, daemon=True).start()

def end_macro():
    config["is_running"] = 0
    update_config()
    sleep(200)  # Allow some time for the loop to stop

    os.execv(sys.executable, [sys.executable, '"' + __file__ + '"'])

def toggle_dark_mode():
    config["darkmode"] = dark_mode_var.get()
    update_config()

    if config["darkmode"]:
        customtkinter.set_appearance_mode('dark')
    else:
        customtkinter.set_appearance_mode('light')

def toggle_auto_macro():
    config["autoclicker"] = auto_macro_var.get()
    update_config()

    if config["autoclicker"]:
        print("Auto Click Macro Enabled") 
    else:
        print("Auto Click Macro Disabled")

def toggle_upgrade_path():
    config["upgrade"] = upgrade_path_var.get()
    update_config()

    if config["upgrade"]:
        print("alright enabled this thing")
    else:
        print("disabled this thing")

def update_upgrade_delay_label(value):
    upgrade_delay_label.configure(text=f"Upgrade Delay: {int(value)} min")
    config["upgrade_delay"] = value
    update_config()

def enter_upgrade():
    move_to(60, 90)
    sleep(500)
    click()
    sleep(500)

def exit_upgrade():
    move_to(47.5, 90)
    sleep(500)
    click()
    sleep(500)

def back_upgrade():
    move_to(55, 90)
    sleep(500)
    click()
    sleep(500)

def find_upgrade_tile():
    for i in range(3):
        xp, yp = find_color("0xFFC400", 19, 0, 90, 100)
        if (xp, yp) == (0, 0):
            print(f"No upgrade tile found... Attempt {i}")
        else:
            print(f"Found upgrade tile!")
            move_to(xp, yp)
            click()
            sleep(1000)
            back_button()
            break

def reset_upgrade_zoom():
    move_to(50, 50)

    for _ in range(10):
        press("i")
    for _ in range(10):
        press("o")

def test_module(): # un upgraded square checker
    search_size = 5
    padx = 18
    pos_list = []
    status = False
    for i in range(15):
        for v in range(20):
            xp, yp = find_color("0x10110E", padx + search_size*(i-1), search_size*(v-1), padx + search_size*(i), search_size*(v))
            if (xp, yp) != (0, 0):
                pos_list.append((xp, yp))
                status = True
                print(f"Chunk {i}, {v}. Status: {status} | {xp, yp}")
                move_to()
            else:
                status = False
                print(f"Chunk {i}, {v}. Status: {status}")

    print(pos_list)

# Register global hotkeys
keyboard.add_hotkey('F1', begin_macro)  # Register F1 to start the macro
keyboard.add_hotkey('F2', end_macro)    # Register F2 to stop the macro
keyboard.add_hotkey('F3', test_module)  # For testing

# Main Tab
main_frame = customtkinter.CTkFrame(tabView.tab("Main"))
main_frame.pack(padx=10, pady=10, fill="both", expand=True)
main_label = customtkinter.CTkLabel(main_frame, text= "Main Settings", font=("Arial", 16))
main_label.pack(pady=(10,5))

upgrade_delay_label = customtkinter.CTkLabel(main_frame, text=f"Upgrade Delay: {int(config["upgrade_delay"])} min", font=("Arial", 12))
upgrade_delay_label.pack(pady=(10, 5))
upgrade_delay_slider = customtkinter.CTkSlider(main_frame, from_=1, to=30, number_of_steps=29, command=update_upgrade_delay_label)
upgrade_delay_slider.pack(pady=(10, 5))
upgrade_delay_slider.set(config["upgrade_delay"])

button_1 = customtkinter.CTkButton(main_frame, text="F1 START", command=begin_macro)
button_1.pack(padx=20, pady=20)
button_2 = customtkinter.CTkButton(main_frame, text="F2 STOP", command=end_macro)
button_2.pack(padx=25, pady=25)


# Settings Tab
settings_frame = customtkinter.CTkFrame(tabView.tab("Settings"))
settings_frame.pack(padx=10, pady=10, fill="both", expand=True)

# GUI Settings Section
gui_label = customtkinter.CTkLabel(settings_frame, text="GUI Settings", font=("Arial", 16))
gui_label.pack(pady=(10, 5))

dark_mode_var = tkinter.IntVar()
dark_mode_var.set(config["darkmode"])
dark_mode_checkbox = customtkinter.CTkCheckBox(settings_frame, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_checkbox.pack(pady=(5, 10))

# Path Settings Section
path_label = customtkinter.CTkLabel(settings_frame, text="Path Settings", font=("Arial", 16))
path_label.pack(pady=(10, 5))

auto_macro_var = tkinter.IntVar()
auto_macro_var.set(config["autoclicker"])
auto_macro_checkbox = customtkinter.CTkCheckBox(settings_frame, text="Auto Click Macro", variable=auto_macro_var, command=toggle_auto_macro)
auto_macro_checkbox.pack(pady=(5, 10))

upgrade_path_var = tkinter.IntVar()
upgrade_path_var.set(config["upgrade"])
upgrade_path_checkbox = customtkinter.CTkCheckBox(settings_frame, text = "Upgrade Path", variable= upgrade_path_var, command= toggle_upgrade_path)
upgrade_path_checkbox.pack(pady=(5, 10))

# Credits Tab
credits_frame = customtkinter.CTkFrame(tabView.tab("Credits"))
credits_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Unique Font Text
credits_label = customtkinter.CTkLabel(credits_frame, text="Credits to steveonly4\nand innocenthuman", font=("Comic Sans MS", 18))
credits_label.pack(pady=(10, 5))

# Load Image
image_path = sys.path[0] + "\\images\\credits.png"  # Path to your image

# Load the image
try:
    image = Image.open(image_path)
    image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(128,99))
    image_label = customtkinter.CTkLabel(credits_frame, text="", image=image)
    image_label.pack(pady=(5, 10))
except tkinter.TclError:
    print("Error loading image. Please check the file path.")

app.mainloop()
