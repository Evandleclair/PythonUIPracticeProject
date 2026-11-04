#__main__.py
import sys, atexit, logging
from Windows.mainWindow import MainWindow


def configure_logging():
    """Sets up a centralized logging service (adhering to SRP)."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger("AppMain")

def exit_method(pWindow, pConfigHelper, pLogger):
    try:
        exportedConfig = pWindow.export_config()
        pConfigHelper.write_config_data(exportedConfig)
    except Exception as e:
        pLogger.error("Failed to save config file during shutdown due to exception: %s",e)
    
    

def main():
    from PyQt5.QtWidgets import QApplication
  
    from Windows.helpers import DirectoryHelper, ConfigHelper
    logger = configure_logging()
    logger.info("Initializing application...")
    directoryHelper = DirectoryHelper()
    configHelper = ConfigHelper("config", directoryHelper.write_file)
    configData = configHelper.startup_get_config_data_and_load_values()
    configResetEvent = lambda: configHelper.reset_config_data() #this is passed seperate from the directory helper in case we ever spin config functions off into their own seperate thing.
    app = QApplication(sys.argv)
    window = MainWindow(configData,directoryHelper, configResetEvent, logger)
    app.aboutToQuit.connect(lambda: exit_method(window, configHelper, logger))
    window.show()  # Windows by default are hidden.
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

       