from UnitConverter import UnitConverter
from GUI import GUI

def main():
    converter = UnitConverter()
    converter.load_units('units.txt')
    app = GUI(converter)
    app.window.mainloop()

if __name__ == "__main__":
    main()