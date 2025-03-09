import tkinter as tk
from gui import AudioProcessorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioProcessorGUI(root)
    root.mainloop()