import tkinter as tk

from manager import FitnessManager
from gui import FitnessApp

def main():
    root = tk.Tk()
    manager = FitnessManager()

    FitnessApp(root, manager)

    root.mainloop()

if __name__ == "__main__":
    main()