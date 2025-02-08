import tkinter as tk
from sticker_maker import StickerMaker

def main() -> str:
    root = tk.Tk()
    app = StickerMaker(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()