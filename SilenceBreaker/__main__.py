#__main__.py
def main():
    from PyQt5.QtWidgets import QApplication
    from Windows.mainWindow import MainWindow
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Windows by default are hidden.
    app.exec()
    
if __name__ == "__main__":
    main()