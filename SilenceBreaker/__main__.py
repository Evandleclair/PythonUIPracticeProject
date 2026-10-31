#__main__.py
import sys, atexit
from Windows.mainWindow import MainWindow

def exit_method(pWindow, pDirectoryHelper):
    exportedConfig = pWindow.export_config()
    pDirectoryHelper.write_config_data(exportedConfig)
    print(exportedConfig)
    

def main():
    from PyQt5.QtWidgets import QApplication
  
    from Windows.helpers import DirectoryHelper
  
    directoryHelper = DirectoryHelper()
    configData = directoryHelper.startup_get_config_data_and_load_values()
    configResetEvent = directoryHelper.reset_config_data() #this is passed seperate from the directory helper in case we ever spin config functions off into their own seperate thing.
    app = QApplication(sys.argv)
    window = MainWindow(configData,directoryHelper, configResetEvent)
    atexit.register(exit_method, window, directoryHelper)
    app.aboutToQuit.connect(lambda: exit_method(window, directoryHelper))
    window.show()  # Windows by default are hidden.
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

       