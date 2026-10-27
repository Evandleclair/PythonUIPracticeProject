#__main__.py
import sys, atexit


def exit_method(pWindow, pDirectoryHelper):
    print('exit')
    

def main():
    from PyQt5.QtWidgets import QApplication
    from Windows.mainWindow import MainWindow
    from Windows.helpers import DirectoryHelper
  
    directoryHelper = DirectoryHelper()
    configData = directoryHelper.startup_get_config_data_and_load_values()
    
    app = QApplication(sys.argv)
    window = MainWindow(configData,directoryHelper)
    atexit.register(exit_method, window, directoryHelper)
    app.aboutToQuit.connect(lambda: exit_method(window, directoryHelper))
    window.show()  # Windows by default are hidden.
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

       