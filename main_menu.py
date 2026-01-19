import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# --- DYNAMIC PATH CONFIGURATION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
cv_projects_root = os.path.dirname(current_dir)

def run_project(file_name, folder_name):
    file_path = os.path.join(cv_projects_root, folder_name, file_name)
    project_folder = os.path.join(cv_projects_root, folder_name)

    if os.path.exists(file_path):
        # This hides the dashboard so only the camera window is visible
        root.withdraw() 
        try:
            # subprocess.run waits here until you close the camera window
            subprocess.run([sys.executable, file_path], cwd=project_folder, check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Project stopped:\n{e}")
        finally:
            # Dashboard reappears automatically when camera window is closed
            root.deiconify() 
    else:
        messagebox.showerror("Path Error", f"File not found: {file_name}")

def quit_dashboard():
    if messagebox.askokcancel("Exit", "Do you want to close the AI Dashboard?"):
        root.destroy()

# --- UI WINDOW ---
root = tk.Tk()
root.title("AI Vision Dashboard")
root.geometry("600x650") # Slightly increased height for the credits
root.configure(bg="#1a1a1a")

# Close dashboard properly if "X" is clicked
root.protocol("WM_DELETE_WINDOW", quit_dashboard)

tk.Label(root, text="AI VISION CONSOLE", font=("Arial", 22, "bold"), 
         bg="#1a1a1a", fg="#00FF00", pady=30).pack()

btn_style = {"font": ("Arial", 12, "bold"), "width": 35, "pady": 10, "cursor": "hand2"}

# --- PROJECT BUTTONS ---
tk.Button(root, text="✨ INVISIBILITY CLOAK", bg="#4b0082", fg="white", **btn_style,
          command=lambda: run_project("Harry_Potter_cloak.py", "AI-Vision-App")).pack(pady=10)

tk.Button(root, text="🎨 AIR CANVAS", bg="#005b96", fg="white", **btn_style,
          command=lambda: run_project("air_canvavs.py", "AI-Vision-App")).pack(pady=10)

tk.Button(root, text="🎵 EMOTION MUSIC PLAYER", bg="#1e8449", fg="white", **btn_style,
          command=lambda: run_project("music_player_webcam.py", "AI-Vision-App")).pack(pady=10)

# --- EXIT BUTTON ---
tk.Button(root, text="❌ EXIT DASHBOARD", bg="#b22222", fg="white", **btn_style,
          command=quit_dashboard).pack(pady=30)

# Instruction label
tk.Label(root, text="Tip: Press 'q' or 'ESC' in the camera window to go back.", 
         bg="#1a1a1a", fg="gray", font=("Arial", 9)).pack(pady=5)

# --- CREDITS LABEL ---
tk.Label(root, text="Created by Archit Yadav", 
         bg="#1a1a1a", fg="#00FF00", font=("Arial", 10, "italic")).pack(side="bottom", pady=20)

root.mainloop()