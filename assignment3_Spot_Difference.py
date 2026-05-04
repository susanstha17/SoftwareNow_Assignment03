import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk

# ---------------- IMAGE PROCESSOR ---------------- #
class ImageProcessor:
    def convert(self, img, size=(400, 400)):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.resize(img, size)
        return ImageTk.PhotoImage(Image.fromarray(img))

# ---------------- GAME LOGIC ---------------- #
class DifferenceGame:
    def __init__(self):
        print("DifferenceGame class initialized")
        # Initialize game state
        self.original = None
        self.modified = None
        self.differences = []
        self.found = []
        self.max_differences = 5
        
    def load_image(self, path):
        img = cv.imread(path)

        if img is None:
            return False

        self.original = img
        self.modified = img.copy()

        return True
    
    # Placeholder for difference generation logic
    def create_differences(self):
        print("Generating differences...")

# ---------------- GAME UI ---------------- #
class GameUI:
    def __init__(self, master):
        print("GameUI class initialized")

        self.master = master
        self.game = DifferenceGame()
        self.processor = ImageProcessor()

        # ---------------- BUTTON FRAME ---------------- #
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.load_button = tk.Button(button_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.reveal_button = tk.Button(button_frame, text="Reveal", command=self.reveal)
        self.reveal_button.pack(side=tk.LEFT, padx=10)

        # ---------------- IMAGE FRAME ---------------- #
        image_frame = tk.Frame(master)
        image_frame.pack()

        self.original_img_label = tk.Label(image_frame)
        self.modified_img_label = tk.Label(image_frame)

        self.original_img_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.modified_img_label.pack(side=tk.RIGHT, padx=10, pady=10)

    # ---------------- LOAD IMAGE ---------------- #
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

        # update UI with images
        self.original_img_label.config(image=tk_img1)
        self.modified_img_label.config(image=tk_img2)

        # keep reference to avoid garbage collection
        self.original_img_label.image = tk_img1
        self.modified_img_label.image = tk_img2
    # ---------------- REVEAL PLACEHOLDER ---------------- #
    def reveal(self):
        print("Reveal button clicked")

# ---------------- MAIN APPLICATION ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spot the Difference")
    root.geometry("900x500")

    app = GameUI(root)
    root.mainloop()