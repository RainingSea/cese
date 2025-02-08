from UnitConverter import UnitConverter
from GUI import GUI

def main():
    converter = UnitConverter()
    converter.load_conversion_factors('conversion_factors.txt')
    app = GUI(converter)
    app.root.mainloop()

if __name__ == "__main__":
    main()