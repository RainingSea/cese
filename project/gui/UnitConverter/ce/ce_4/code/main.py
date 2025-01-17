from conversion import UnitConverter
from gui import GUI

def main():
    converter = UnitConverter()
    converter.load_conversion_factors('conversion_factors.txt')
    app = GUI(converter)
    app.root.mainloop()

if __name__ == "__main__":
    main()