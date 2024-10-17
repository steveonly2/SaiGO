from lib.controls_module import * # modules in /lib
from paths.vending_machine import *

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
app = customtkinter.CTk()
app.geometry("500x500")

tabView = customtkinter.CTkTabview(app)
tabView.pack(padx=20, pady=20)
tabView.add("Main")
tabView.add("Settings")
tabView.add("Credits")
tabView.add("Webhook")

default_settings = {
    "version": "v1.3",
    "is_running": 0,
    "autoclicker_running": 0,

    "darkmode_enabled": 0,
    "autoclicker_enabled": 0,
    "upgrade_enabled": 0,
    "vending_enabled" : 0,
    "screenshot_enabled" : 0,
    "webhook_enabled" : 0,

    "upgrade_delay": 5,
    "upgrade_startpos": 1,
    "upgrade_cooldown": 0,

    "vending_delay": 10,
    "vending_cooldown": 0
    }

# -------- CONFIGS -------- #


for _ in range(2):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            break
    except FileNotFoundError:
        with open(config_path, 'w') as f:
            json.dump(default_settings, f)

if config["darkmode_enabled"]:
    customtkinter.set_appearance_mode('dark')

def update_config():
    with open(config_path, 'w') as f:
        json.dump(config, f)

app.title(f"SaiGO {config["version"]}")

# -------- MAIN LOOPS -------- #


def mainLoop():
    while config["is_running"]:

        if config["upgrade_enabled"]:
            if config["upgrade_cooldown"] == 0:
                update_config()
                enter_upgrade()
                sleep(1000)
                startpos = get_upgrade_startpos()
                sleep(1000)

                if startpos != 1:
                    go_to_startpos(1, True)

                if startpos == 1:
                    upgrade_tile()
                    sleep(500)
                
                config["upgrade_cooldown"] = config["upgrade_delay"]*60
        
        if config["vending_enabled"]:
            if config["vending_cooldown"] == 0:
                walk_to_vending_machine()
                sleep(500)
                open_vending_machine()

                if vending_machine_check():
                    for _ in range(6):
                        buy_potion()
                        sleep(2500)
                
                reset_from_vending_machine()
                config["vending_cooldown"] = config["vending_delay"]*60
                sleep(1000)

        if config["autoclicker_enabled"]:
            config["autoclicker_running"] = 1
            update_config()

            while config["upgrade_cooldown"] or not config["upgrade_enabled"]:
                click_loop()

            sleep(1500)
        
        sleep(100)
                
def secLoop():
    while config["is_running"]:

        if config["upgrade_enabled"]:
            if config["upgrade_cooldown"] != 0:
                config["upgrade_cooldown"] -= 1
            else:
                if config["autoclicker_enabled"]:
                    config["autoclicker_running"] = 0
        
        if config["vending_enabled"]:
            if config["vending_cooldown"] !=0:
                config["vending_cooldown"] -= 1
            else:
                if config["autoclicker_enabled"]:
                    config["autoclicker_running"] = 0

        sleep(1000)
        update_config()


# -------- AUTOMATIONS -------- #


def click_loop():
    if config["autoclicker_enabled"]:
        while config["autoclicker_running"]:
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

    reset_zoom()
    enable_autoroll()

    enter_upgrade()
    reset_upgrade_zoom()
    for _ in range(2):
        if back_button_exists() == True:
            back_upgrade()
            sleep(2000)

    if get_upgrade_startpos() == 0:
        find_upgrade_tile()
    
    sleep(1500)
    go_to_startpos(1)

    exit_upgrade()

    print("Macro Started")
        
    # Start the clicking loop in a new thread
    threading.Thread(target=mainLoop, daemon=True).start()
    threading.Thread(target=secLoop, daemon=True).start()

def end_macro():
    config["is_running"] = 0
    update_config()
    sleep(200)  # Allow some time for the loop to stop

    os.execv(sys.executable, [sys.executable, '"' + __file__ + '"'])

def toggle_screenshot_function():
    screenshot(screenshot_path)

def toggle_dark_mode():
    config["darkmode_enabled"] = dark_mode_var.get()
    update_config()

    if config["darkmode_enabled"]:
        customtkinter.set_appearance_mode('dark')
    else:
        customtkinter.set_appearance_mode('light')

def toggle_auto_macro():
    config["autoclicker_enabled"] = auto_macro_var.get()
    update_config()

    if config["autoclicker_enabled"]:
        print("Auto Click Macro Enabled") 
    else:
        print("Auto Click Macro Disabled")

def toggle_upgrade_path():
    config["upgrade_enabled"] = upgrade_path_var.get()
    update_config()

    if config["upgrade_enabled"]:
        print("alright enabled this thing")
    else:
        print("disabled this thing")

def toggle_vending_path():
    config["vending_enabled"] = vending_path_var.get()
    update_config()

    if config["vending_enabled"]:
        print("enabled vending path")
    else:
        print("disabled vending path")

def toggle_webhook():
    config["webhook_enabled"] = webhook_var.get()
    update_config()

    if config['webhook_enabled']:
        print('enabled ')
    else:
        print('disabled')



def enable_autoroll():
    if autoroll_check() == False:
        move_to(50, 87.5)
        click()
        sleep(300)
        move_to(22, 88)
        click()
        sleep(200)
        move_to(79.4, 88)
        click()

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
            back_upgrade()
            return True
    return False

def find_upgradeable_tile():
    sizex = 5.5
    sizey = 7
    padx = 18
    pady = 8
    pos_list = []
    status = False
    for i in range(12):
        for v in range(13):
            xp, yp = find_color("0x10110E", padx + sizex*(i-1), pady + sizey*(v-1), padx + sizex*(i), pady + sizey*(v))
            if (xp, yp) != (0, 0):
                pos_list.append((xp, yp))
                status = True
                print(f"Chunk {i}, {v}. Status: {status} | {xp, yp}")
            else:
                status = False
                print(f"Chunk {i}, {v}. Status: {status}")

    return pos_list

def upgrade_tile():
    unupgraded_tiles = find_upgradeable_tile()
    for i in unupgraded_tiles:
        move_to(i[0], i[1])
        click()
        if affordable_check() == False:
            move_to(50, 76)
            click()
        
        sleep(200)
        back_upgrade()
        move_to(50,50)
        sleep(1000)
        click()
        sleep(2000)


def reset_upgrade_zoom():
    move_to(50, 50)

    for _ in range(10):
        press("o")

def reset_zoom():
    move_to(50, 50)

    for _ in range(10):
        press("o")
    
    mouse_hold("R")
    move_to(50, 70)
    mouse_release("R")

def test_module():
    unupgraded_tiles = find_upgradeable_tile()
    for i in unupgraded_tiles:
        move_to(i[0], i[1])
        click()
        if affordable_check() == False:
            move_to(50, 76)
            click()
        
        sleep(200)
        back_upgrade()
        move_to(50,50)
        sleep(1000)
        click()
        sleep(2000)

def test_module():
    print(affordable_check())

def get_pos_info():
    x, y = mouse_pos()
    print(f"{mouse_pos()} | {getcolor(x, y)}")

# Register global hotkeys
keyboard.add_hotkey('F1', begin_macro)  # Register F1 to start the macro
keyboard.add_hotkey('F2', end_macro)    # Register F2 to stop the macro
keyboard.add_hotkey('F3', test_module)  # For testing
keyboard.add_hotkey('F5', get_pos_info)


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

screenshoot_function_var = tkinter.IntVar()
screenshoot_function_var.set(config["screenshot_enabled"])
screenshot_function_checkbox = customtkinter.CTkCheckBox(main_frame, text="Dark Mode", variable=screenshoot_function_var, command=toggle_screenshot_function)
screenshot_function_checkbox.pack(pady=(5, 10))

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
dark_mode_var.set(config["darkmode_enabled"])
dark_mode_checkbox = customtkinter.CTkCheckBox(settings_frame, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_checkbox.pack(pady=(5, 10))

# Path Settings Section
# Path Label
path_label = customtkinter.CTkLabel(settings_frame, text="Path Settings", font=("Arial", 16))
path_label.pack(pady=(10, 5))

# Create a frame to hold the checkboxes side by side
checkbox_frame = customtkinter.CTkFrame(settings_frame)
checkbox_frame.pack(pady=(5, 10), fill="x")  # Align checkboxes in this frame

# Auto Click Macro Checkbox
auto_macro_var = tkinter.IntVar()
auto_macro_var.set(config["autoclicker_enabled"])
auto_macro_checkbox = customtkinter.CTkCheckBox(checkbox_frame, text="Auto Click Macro", variable=auto_macro_var, command=toggle_auto_macro)
auto_macro_checkbox.pack(side="left", padx=(10, 10))

# Upgrade Path Checkbox
upgrade_path_var = tkinter.IntVar()
upgrade_path_var.set(config["upgrade_enabled"])
upgrade_path_checkbox = customtkinter.CTkCheckBox(checkbox_frame, text="Upgrade Path", variable=upgrade_path_var, command=toggle_upgrade_path)
upgrade_path_checkbox.pack(side="left", padx=(10, 10))

# Auto Use Vending Machine Checkbox
vending_path_var = tkinter.IntVar()
vending_path_var.set(config["vending_enabled"])
vending_path_checkbox = customtkinter.CTkCheckBox(checkbox_frame, text="Auto Use Vending Machine", variable=vending_path_var, command=toggle_vending_path)
vending_path_checkbox.pack(side="left", padx=(10, 10))

# Credits Tab
credits_frame = customtkinter.CTkFrame(tabView.tab("Credits"))
credits_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Unique Font Text
credits_label = customtkinter.CTkLabel(credits_frame, text="Credits to steveonly4\nand innocenthuman", font=("Comic Sans MS", 18))
credits_label.pack(pady=(10, 5))


# webhook tab
webhook_frame = customtkinter.CTkFrame(tabView.tab("Webhook"))
webhook_frame.pack(padx=10, pady=10, fill="both", expand=True)
webhook_label = customtkinter.CTkLabel(webhook_frame, text= "Webhook Settings", font=("Arial", 16))
webhook_label.pack(pady=(10,5))

webhook_var = tkinter.IntVar()
webhook_var.set(config["webhook_enabled"])
webhook_url_input_checkbox = customtkinter.CTkCheckBox(webhook_frame, text="Enable Webhook", variable=webhook_var, command=toggle_webhook)
webhook_url_input_checkbox.pack(side="left", padx=(10, 10))


# Load the image
try:
    image = Image.open(image_path)
    image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(128,99))
    image_label = customtkinter.CTkLabel(credits_frame, text="", image=image)
    image_label.pack(pady=(5, 10))
except tkinter.TclError:
    print("Error loading image. Please check the file path.")

app.mainloop()
