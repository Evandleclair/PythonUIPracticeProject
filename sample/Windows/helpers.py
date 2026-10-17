from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton,QDial, QSlider, QLabel, QVBoxLayout, QHBoxLayout, QSlider,QLayout,QGridLayout
from PyQt5.QtCore import Qt

class Color(QWidget):
    def __init__(self, pColor):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(pColor))
        self.setPalette(palette)

class QWidgetHelper():
    @staticmethod
    def GenerateButton(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget

    @staticmethod
    def GenerateButton(pText,pEvent):
        returnWidget = QPushButton(pText)
        returnWidget.clicked.connect(pEvent)
        return returnWidget
    
    @staticmethod
    def GenerateSlider(pEvent, pMin, pMax):
        returnWidget = QSlider(Qt.Horizontal)
        returnWidget.sliderMoved.connect(pEvent)
        returnWidget.setMinimum(pMin)
        returnWidget.setMaximum(pMax)
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
    def GenerateVolumeSection(pLabelText, pVolumeVariable):
        widgetList = []
        widgetList.append(QWidgetHelper.GenerateLabel(pLabelText))
        widgetList.append(QWidgetHelper.VolumeLabel(pVolumeVariable))
        returnWidget = QWidgetHelper.GenerateVBoxLayout(widgetList)
        return returnWidget

    @staticmethod
    def GenerateChanceSlider(pLabelText, pEvent):
        widgetList=[]
        widgetList.append(QWidgetHelper.GenerateLabel(pLabelText))
        widgetList.append(QWidgetHelper.GenerateSlider(pEvent,0,100))
        returnWidget = QWidgetHelper.GenerateHBoxLayout(widgetList)
        return returnWidget
    
    @staticmethod 
    def GenerateHBoxLayout(widgets =[],*args):
        returnWidget = QHBoxLayout()
        for widget in widgets:
            if isinstance(widget, QWidget):
                returnWidget.addWidget(widget)
            elif isinstance(widget, QLayout):
                returnWidget.addLayout(widget)      
        return returnWidget

    @staticmethod 
    def GenerateVBoxLayout(widgets =[], *args):
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
    def GenerateDial(pEvent):
        returnWidget = QDial()
        return returnWidget

class GridUIElement():
    def __init__(self, pElement, pRow, pCol):
        self.element = pElement
        self.row = pRow
        self.col = pCol
