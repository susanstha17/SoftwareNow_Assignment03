import random
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk

# ---------------- IMAGE PROCESSOR ---------------- #
# This class handles image conversion for displaying
# OpenCV images inside Tkinter canvases
class ImageProcessor:
    
    # Convert OpenCV image into Tkinter compatible image
    def convert(self, img, size=(400, 400)):
        
        # Convert image from BGR (OpenCV default)
        # to RGB format for Tkinter display
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        # Resize image so both images fit properly in GUI
        img = cv.resize(img, size)
        
        # Convert NumPy array into Tkinter-compatible image
        return ImageTk.PhotoImage(Image.fromarray(img))

# --- GAME LOGIC --- #
# This class contains all game logic including:
# - image loading
# - difference generation
# - click checking
# - tracking found differences
class DifferenceGame:
    
    def __init__(self):
        print("DifferenceGame class initialized")
        # Store original image
        self.original = None
        
        # Store modified image with differences
        self.modified = None
        
        # Store coordinates of generated differences
        self.differences = []
        
        # Store indexes of already found differences
        self.found = []
        
        # Total number of differences to generate
        self.max_differences = 5

    # function to load image and generate differences
    def load_image(self, path):
        img = cv.imread(path)

        if img is None:
            return False

        self.original = img
        self.modified = img.copy()

        self.create_differences()

        return True
    
    # function to create differences on the modified image
    def create_differences(self):
        self.modified = self.original.copy()
        self.differences = []
        self.found = []

        h, w = self.original.shape[:2]

        attempts = 0

        # Continue until required differences are created
        while len(self.differences) < self.max_differences and attempts < 200:
            x = random.randint(50, w - 50)
            y = random.randint(50, h - 50)

            # avoid overlap between differences
            if all(abs(x - dx) > 60 and abs(y - dy) > 60 for dx, dy in self.differences):

                # apply visible difference
                self.apply_change(x, y)

                self.differences.append((x, y))

            attempts += 1
    
    # function to check if click is on a difference
    def check_click(self, x, y):
        for i, (dx, dy) in enumerate(self.differences):
            if i in self.found:
                continue

            # Check if user clicked close to difference
            if abs(x - dx) < 30 and abs(y - dy) < 30:
                self.found.append(i)
                return True, (dx, dy)

        return False, None
    
    # function to apply a random change at the given coordinates
    def apply_change(self, x, y):
        choice = random.choice(["circle", "rectangle", "invert"])

        if choice == "circle":
            cv.circle(self.modified, (x, y), 25, (0, 0, 255), -1)

        elif choice == "rectangle":
            cv.rectangle(self.modified, (x - 25, y - 25), (x + 25, y + 25), (0, 255, 0), -1)

        elif choice == "invert":
            roi = self.modified[y - 25:y + 25, x - 25:x + 25]
            self.modified[y - 25:y + 25, x - 25:x + 25] = 255 - roi

# ---------------- GAME UI ---------------- #
class GameUI:
    # Initialize the UI and game logic
    def __init__(self, master):
        print("GameUI class initialized")
        self.mistakes = 0
        self.max_mistakes = 3
        self.game_over = False
        self.master = master
        self.game = DifferenceGame()
        self.processor = ImageProcessor()

        # ---------------- BUTTON FRAME ---------------- #
        # Frame used to organize top control buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        
        # create buttons
        self.load_button = tk.Button(button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)
        
        self.reveal_button = tk.Button(button_frame, text="Reveal", command=self.reveal)
        self.reveal_button.pack(side=tk.LEFT, padx=10)
        # create status label
        self.status_label = tk.Label(master, text="Load an image to start")
        self.status_label.pack()
        
        # ---------------- IMAGE FRAME ---------------- #
        image_frame = tk.Frame(master)
        image_frame.pack()

        # create canvases for original and modified images
        self.canvas1 = tk.Canvas(image_frame, width=400, height=400, bg="gray")
        self.canvas2 = tk.Canvas(image_frame, width=400, height=400, bg="gray")
        # pack canvases side by side
        self.canvas1.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas2.pack(side=tk.RIGHT, padx=10, pady=10)

        # click detection on modified image
        self.canvas2.bind("<Button-1>", self.on_click)

    # ---------------- LOAD IMAGE ---------------- #
    # function to load image and update UI
    def load_image(self):
        print("Load image button clicked")
        # Open file dialog to select image
        path = filedialog.askopenfilename()

        if not path:
            return

        # load image into game logic
        if not self.game.load_image(path):
            messagebox.showerror("Error", "Failed to load image")
            return

        # convert images for display
        tk_img1 = self.processor.convert(self.game.original)
        tk_img2 = self.processor.convert(self.game.modified)

        # clear old drawings/images
        self.canvas1.delete("all")
        self.canvas2.delete("all")

        # display images
        self.canvas1.create_image(0, 0, anchor="nw", image=tk_img1)
        self.canvas2.create_image(0, 0, anchor="nw", image=tk_img2)

        # keep references
        self.canvas1.image = tk_img1
        self.canvas2.image = tk_img2
       
        # reset game state
        self.mistakes = 0
        self.update_status()
        self.game_over = False

    # ---------------- CHECK CLICK ---------------- #
    # function to check if click is on a difference
    def on_click(self, event):
        print("Image clicked")
        # ignore clicks if game is over
        if self.game_over:
            messagebox.showinfo("Game Over", "Please load a new image to play again.")
            return
        # ignore clicks if no image loaded
        if self.game.original is None:
            return

        # Get original image size
        h, w = self.game.original.shape[:2]

        # Convert click position (UI → actual image)
        x = int(event.x * w / 400)
        y = int(event.y * h / 400)

        correct, pos = self.game.check_click(x, y)

        if correct:
            self.draw_circle(pos, "red")
        else:
            self.mistakes += 1
            messagebox.showwarning("Wrong", f"Mistakes: {self.mistakes}/{self.max_mistakes}")

        self.update_status()
        self.check_game()
        
    # function to draw a circle on the modified image at the given position
    def draw_circle(self, pos, color):
        x, y = pos

        h, w = self.game.original.shape[:2]

        # convert actual image coordinates → canvas coordinates
        x = int(x * 400 / w)
        y = int(y * 400 / h)

        # draw on both canvases
        self.canvas1.create_oval(
            x - 15, y - 15,
            x + 15, y + 15,
            outline=color,
            width=3
        )
        # draw on modified image canvas
        self.canvas2.create_oval(
            x - 15, y - 15,
            x + 15, y + 15,
            outline=color,
            width=3
        )
    # function to update the status label with remaining differences and mistakes
    def update_status(self):
        remaining = self.game.max_differences - len(self.game.found)
        self.status_label.config(
            text=f"Remaining: {remaining} | Mistakes: {self.mistakes}/{self.max_mistakes}"
        ) 

    # function to check if game is over or won
    def check_game(self):
        # check if too many mistakes
        if self.mistakes >= self.max_mistakes:
            self.game_over = True
            messagebox.showerror("Game Over", "Too many mistakes!")
            return
         # Win game if all differences found
        if len(self.game.found) == self.game.max_differences:
            self.game_over = True
            messagebox.showinfo("Success", "You found all differences!")    
    
    # function to reveal all remaining differences by drawing blue circles
    def reveal(self):
        if self.game.original is None:
            return
        # draw blue circles on all remaining differences
        for i, pos in enumerate(self.game.differences):
            if i not in self.game.found:
                self.draw_circle(pos, "blue")

# ---------------- MAIN APPLICATION ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spot the Difference")
    root.geometry("900x500")

    app = GameUI(root)
    # Start Tkinter event loop
    root.mainloop()