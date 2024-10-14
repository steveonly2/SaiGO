import customtkinter
import pyautogui
import tkinter
import os
import sys
import time
import threading
import keyboard  

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

is_macro_running = False
def get_target_coordinates():
    # Get the screen size
    screen_width, screen_height = pyautogui.size()
    
    # Calculations (idk how the calculations actually work don't ask me)
    x = int(screen_width * 0.55)  
    y = int(screen_height * 0.85)  
    return x, y

def click_loop():
    global is_macro_running
    while is_macro_running:
        try:
            x,y = get_target_coordinates()
            pyautogui.moveTo(x,y)  # Move to the specified coordinates
            pyautogui.click()  # Click
            time.sleep(0.1)  # Small delay between clicks
        except OverflowError:
            print("Overflow error in clicking")
            break  # Exit the loop if there's an error

def begin_macro():
    global is_macro_running
    if auto_macro_var.get() == 1:
        is_macro_running = True  # Set the control variable to True
        print("Auto Click Macro started")
        
        # Start the clicking loop in a new thread
        threading.Thread(target=click_loop, daemon=True).start()
    else:
        print("Please select a path from settings")

def end_macro():
    global is_macro_running
    is_macro_running = False
    time.sleep(0.2)  # Allow some time for the loop to stop

    os.execv(sys.executable, ['python'] + sys.argv)

def toggle_dark_mode():
    if dark_mode_var.get() == 1:
        customtkinter.set_appearance_mode('dark')
    else:
        customtkinter.set_appearance_mode('light')

def toggle_auto_macro():
    if auto_macro_var.get() == 1:
        print("Auto Click Macro Enabled")
    else:
        print("Auto Click Macro Disabled")

# Register global hotkeys
keyboard.add_hotkey('F1', begin_macro)  # Register F1 to start the macro
keyboard.add_hotkey('F2', end_macro)    # Register F2 to stop the macro

# Main Tab
button_1 = customtkinter.CTkButton(tabView.tab("Main"), text="F1 START", command=begin_macro)
button_1.pack(padx=20, pady=20)
button_2 = customtkinter.CTkButton(tabView.tab("Main"), text="F2 STOP", command=end_macro)
button_2.pack(padx=30, pady=30)

# Settings Tab
settings_frame = customtkinter.CTkFrame(tabView.tab("Settings"))
settings_frame.pack(padx=10, pady=10, fill="both", expand=True)

# GUI Settings Section
gui_label = customtkinter.CTkLabel(settings_frame, text="GUI Settings", font=("Arial", 16))
gui_label.pack(pady=(10, 5))

dark_mode_var = tkinter.IntVar()
dark_mode_checkbox = customtkinter.CTkCheckBox(settings_frame, text="Dark Mode", variable=dark_mode_var, command=toggle_dark_mode)
dark_mode_checkbox.pack(pady=(5, 20))

# Path Settings Section
path_label = customtkinter.CTkLabel(settings_frame, text="Path Settings", font=("Arial", 16))
path_label.pack(pady=(10, 5))

auto_macro_var = tkinter.IntVar()
auto_macro_checkbox = customtkinter.CTkCheckBox(settings_frame, text="Auto Click Macro", variable=auto_macro_var, command=toggle_auto_macro)
auto_macro_checkbox.pack(pady=(5, 20))

# Credits Tab
credits_frame = customtkinter.CTkFrame(tabView.tab("Credits"))
credits_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Unique Font Text
credits_label = customtkinter.CTkLabel(credits_frame, text="Credits To steveonly4", font=("Comic Sans MS", 24))
credits_label.pack(pady=(10, 5))

# Load Image
image_path = r"C:\SaiGO\images\credits.png"  # Path to your image

# Load the image
try:
    image = tkinter.PhotoImage(file=image_path)
    image_label = customtkinter.CTkLabel(credits_frame, image=image)
    image_label.pack(pady=(5, 10))
except tkinter.TclError:
    print("Error loading image. Please check the file path.")

app.mainloop()