#__main__.py
import sys, yaml
def main():
    from PyQt5.QtWidgets import QApplication
    from Windows.mainWindow import MainWindow

    with open(r"config\defaultConfig.yaml", "r") as file:
        configData = yaml.safe_load(file)
    print(configData)
    app = QApplication(sys.argv)
    window = MainWindow(configData)
    window.show()  # Windows by default are hidden.
    app.exec()
    
if __name__ == "__main__":
    main()