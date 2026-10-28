from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton,QDial, QSlider, QLabel, QVBoxLayout, QHBoxLayout, QSlider,QLayout,QGridLayout, QSpinBox,QMessageBox 
from PyQt5.QtCore import Qt
from pathlib import Path
import os, random, zipfile, yaml
import simplejson as json

class Color(QWidget):
    def __init__(self, pColor):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(pColor))
        self.setPalette(palette)

class QWidgetHelper():
    @staticmethod
    def generate_button(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget

    @staticmethod
    def generate_button(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget
    
    @staticmethod
    def GenerateSlider(pEvent,pInitialValue, pMin, pMax):
        returnWidget = QSlider(Qt.Horizontal)
        returnWidget.sliderMoved.connect(pEvent)
        returnWidget.setMinimum(pMin)
        returnWidget.setMaximum(pMax)
        returnWidget.setValue(pInitialValue)
        return returnWidget

    @staticmethod
    def GenerateLabel(pText):
        returnWidget = QLabel(pText)
        return returnWidget

    @staticmethod
    def VolumeLabel(pText):
        returnWidget = QLabel(pText)
        return returnWidget

    @staticmethod
    def generate_volume_section(pLabel, pVolumeVariable):
        widgetList = []
        widgetList.append(QWidgetHelper.GenerateLabel("Volume"))
        widgetList.append(pLabel)
        returnWidget = QWidgetHelper.generate_vbox_layout(widgetList)
        return returnWidget

    @staticmethod
    def generate_interval_section(pMinInterval, pMaxInterval):
        widgetList = []
        minLabel = QWidgetHelper.GenerateLabel("Min Interval")
        maxLabel = QWidgetHelper.GenerateLabel("Max Interval")
        widgetList.append(QWidgetHelper.generate_hbox_layout({minLabel,pMinInterval}))
        widgetList.append(QWidgetHelper.generate_hbox_layout({maxLabel,pMaxInterval}))
        returnWidget = QWidgetHelper.generate_hbox_layout(widgetList)
        return returnWidget

    @staticmethod 
    def generate_interval_spin(pIntervalVar,pIntervalEvent):
        returnwidget = QSpinBox()
        returnwidget.setGeometry(100,100,140,40)
        returnwidget.setValue(pIntervalVar)
        returnwidget.valueChanged.connect(pIntervalEvent)
        returnwidget.setMinimum(0)
        return returnwidget

    @staticmethod
    def generate_chance_slider(pLabelText, pInitialValue, pEvent):
        widgetList=[]
        textLabel = QWidgetHelper.GenerateLabel(pLabelText)
        volNumberLabel = QWidgetHelper.GenerateLabel("0")
        sliderWidget = QWidgetHelper.GenerateSlider(pEvent,pInitialValue,0,100)
        widgetList.append(textLabel)
        widgetList.append(sliderWidget)
        widgetList.append(volNumberLabel)
        returnWidget = QWidgetHelper.generate_hbox_layout(widgetList)
        return returnWidget, volNumberLabel, sliderWidget
    
    @staticmethod 
    def generate_hbox_layout(widgets =[],*args):
        returnWidget = QHBoxLayout()
        for widget in widgets:
            if isinstance(widget, QWidget):
                returnWidget.addWidget(widget)
            elif isinstance(widget, QLayout):
                returnWidget.addLayout(widget)      
        return returnWidget

    @staticmethod 
    def generate_vbox_layout(widgets =[], *args):
        returnWidget = QVBoxLayout()
        for widget in widgets:
            if isinstance(widget, QWidget):
                returnWidget.addWidget(widget)
            elif isinstance(widget, QLayout):
                returnWidget.addLayout(widget)      
        return returnWidget

    @staticmethod
    def GenerateGridLayout(pObjectList=[], *args):
        retLayout = QGridLayout()
        for obj in pObjectList:
            if isinstance(obj.element, QWidget):
                retLayout.addWidget(obj.element,obj.row,obj.col)
            elif isinstance(obj.element, QLayout):
                retLayout.addLayout(obj.element,obj.row,obj.col)      
                
        return retLayout

    @staticmethod
    def generate_dial(pVolumeEvent,pDefaultVolume):
        returnWidget = QDial()
        returnWidget.setRange(0,100)
        returnWidget.setSingleStep(1)
        returnWidget.setValue(pDefaultVolume)
        returnWidget.sliderMoved.connect(pVolumeEvent)
        return returnWidget
    
    @staticmethod
    def generate_and_show_alert(pText):
        dlg = QMessageBox()
        dlg.setText(pText)
        dlg.exec()

class DataHelpers():
    def exclude_key(pDictionary, pKeysToExclude):
       if not isinstance(pKeysToExclude, (list, set, tuple, dict)):
        pKeysToExclude = {pKeysToExclude}
        return {x: pDictionary[x] for x in pDictionary if x not in pKeysToExclude}

    def combine_values(pDictionary):
        returnValue = 0
        for key, value in pDictionary.items():
            returnValue += value
        return returnValue
    
    def pick_random(pDictionary):
        chanceDictionary = DataHelpers.generate_chance_dictionary(pDictionary)

        print(chanceDictionary.items())

        if chanceDictionary[0][2] is None:
            raise ValueError
        while True:
            r = random.random()
            print(f"random chance was {r}")
            for key, value in chanceDictionary.items():
              
                lowOdds = value[0]
                highOdds = value[1]
                print(f"checking {key} with odds of {lowOdds} and {highOdds}")
                if lowOdds <= r <highOdds:
                    print(f"which was between {lowOdds} and {highOdds} resulting in {key}")
                    return key

    @staticmethod 
    def generate_chance_dictionary(pDictionary):
        x=0.0
        chanceDictionary = {}
        for id, chance in pDictionary.items():
            lowOdds = x/100
            highOdds = (x + chance)/100
            newTuple = (lowOdds, highOdds, id)
            chanceDictionary[id]=(newTuple)
            x+=chance
        return chanceDictionary



class GridUIElement():
    def __init__(self, pElement, pRow, pCol, pName = "none"):
        self.element = pElement
        self.row = pRow
        self.col = pCol
        self.name = pName #unique identifier

class DirectoryHelper():
    
    def __init__(self, project_name="SilenceBreaker", default_folder_name="LaughTrack", default_config_folder_name="config"):
        self.home_dir = Path.home()
        self.project_name = project_name
        self.default_sound_folder_name = default_folder_name
        self.default_config_folder_name = default_config_folder_name
        self.default_config_file_name = "config.json"
        self.documents_dir = self.home_dir / "Documents" / self.project_name
        self.current_dir = self.documents_dir

    def establish_core_sound_directories(self, pChanceDirectories):
        establishSounds = False
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        default_noise_folder = self.documents_dir / self.default_sound_folder_name

        if not default_noise_folder.exists():
            establishSounds = True

        default_noise_folder.mkdir(parents=True,exist_ok=True)

        if establishSounds:
            self.copy_sounds_to_default_directory()

        self.current_dir = default_noise_folder
        self.create_sound_subfolders(pChanceDirectories)

    def establish_config_directories(self, pConfigData):
        default_config_folder = self.get_config_path()
        default_config_file = self.get_config_file_path()
        establishConfigs = False
        default_config_folder.mkdir(parents=True,exist_ok=True)
        if not default_config_file.exists() or default_config_file.stat().st_size == 0 or not self.is_valid_json_file(default_config_file): #if file doesnt exist or is empty.
            self.write_config_data(pConfigData, default_config_file)

    @staticmethod
    def is_valid_json_file(pPath):
        try:
            with open(pPath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Invalid JSON! Error: {e}")
            return False
    
    def write_config_data(self,pConfigData, pPath):
        json_str = json.dumps(pConfigData, indent=4)
        pPath.touch(exist_ok=True)
        with open(pPath, "w", encoding="utf-8") as json_file:
            json_file.write(json_str)

    def startup_get_config_data_and_load_values(self):
        configData = self.load_default_config()
        self.establish_config_directories(configData)
        return self.get_config_data(self.get_config_file_path())

    def reset_config_data(self):
        self.write_config_data(self.load_default_config(), self.get_config_file_path())
    
    def load_default_config(self):
        configData = {}
        with open(r"config\defaultConfig.yaml", "r") as file:
            configData = yaml.safe_load(file)
        return configData
    
    def get_config_data(self, pPath):
        with open(pPath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
        
    def copy_sounds_to_default_directory(self):
        print("not implemented")

    def get_random_file(self, pSubFolder):
        p = Path(self.current_dir / pSubFolder).glob('**/*')
        files = [x for x in p if x.is_file()]
        return random.choice(files)

    def etablish_new_sound_folder(self, pNewDirectoryPath):
        print("not implemented")

    def create_sound_subfolders(self, pChanceDirectories):
        for subDir in pChanceDirectories.values():
            noise_subfolder = self.current_dir / subDir
            noise_subfolder.mkdir(parents=True,exist_ok=True)

    def check_sound_folder_exists(self):
        print(self.current_dir)
        return os.path.isdir(self.current_dir)

    def get_working_directory(self):
        return self.current_dir

    def get_config_path(self):
        return self.documents_dir / self.default_config_folder_name

    def get_config_file_path(self):
        return self.get_config_path() / self.default_config_file_name