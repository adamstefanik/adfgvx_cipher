import tkinter as tk
from gui import AdfgvxCipherGUI

def main():
    root = tk.Tk()
    app = AdfgvxCipherGUI(root)
    app.mainloop()

if __name__ == "__main__":
    main()