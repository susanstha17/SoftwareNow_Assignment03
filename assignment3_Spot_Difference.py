import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk
import random

# ---------------- IMAGE PROCESSOR ---------------- #
class ImageProcessor:
    print("ImageProcessor class initialized")

# ---------------- GAME LOGIC ---------------- #
class DifferenceGame:
    def __init__(self):
        print("DifferenceGame class initialized")


# ---------------- GAME UI ---------------- #
class GameUI:
    def __init__(self, master):
        print("GameUI class initialized")
        


#----------------- MAIN APPLICATION ---------------- #
if __name__ == "__main__":
    # Start the game
    root = tk.Tk()
    # Set window title and size
    root.title("Spot the Difference")
    root.geometry("900x500")
    # Create and run the game UI
    app = GameUI(root)
    # Start the Tkinter event loop
    root.mainloop()