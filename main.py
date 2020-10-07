from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
import os
from urllib import request
from urllib.parse import urlparse
from urllib.request import urlopen
from html.parser import HTMLParser 
from pyffmpeg import FFmpeg
import threading
import webbrowser
#pytube is a library under MIT license every right belongs to the author

def scrap(name):
    try:
        html = urlopen(name) 
        f=html.read().decode("utf-8")
        a=f.find(',"commandMetadata":{"webCommandMetadata":{"url":"/watch?v=')+58
        return f[a:a+11]
    except:
        oneSong(name)

def download(url,nome):
    try:
        video = YouTube(url).streams.filter(only_audio = True).first() # MP3
        out_file = video.download()
        base = os.path.splitext(out_file)                
        convert(base[0])
        os.remove(base[0]+'.mp4')       
    except:
        oneSong(nome)
    
def convert(base):   
    ff=FFmpeg()
    ff.convert(base+'.mp4', base+'.mp3')


def oneSong(nome):
    base="https://www.youtube.com/"
    search=base+"results?search_query="
    watch=base+"watch?v="
    for c in nome:
        if ord(c)<128:
            search+=c
    download(watch+scrap(search.replace(" ","+")),nome)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(357, 534)
        MainWindow.setMinimumSize(QtCore.QSize(357, 534))
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.songEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.songEdit.setObjectName("songEdit")
        self.horizontalLayout.addWidget(self.songEdit)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolButton = QtWidgets.QPushButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)
        self.toolButton.clicked.connect(self.about_clicked)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.clicked.connect(self.download_clicked)
        self.verticalLayout.addWidget(self.downloadButton)
        self.infoButton = QtWidgets.QPushButton(self.centralwidget)
        self.infoButton.setObjectName("infoButton")
        self.infoButton.clicked.connect(self.info_clicked)
        self.verticalLayout.addWidget(self.infoButton)
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(self.exit_clicked)
        self.verticalLayout.addWidget(self.exitButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 357, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def download_event(self):
        songList=self.songEdit.toPlainText().splitlines()
        if "" in songList:
            songList.remove("")
        for i, song in enumerate(songList):
            oneSong(song)
            self.progressBar.setValue(int((i+1)*100/len(songList)))  

    def download_clicked(self):
        self.downloadButton.setEnabled(False)
        self.exitButton.setEnabled(False)
        self.songEdit.setEnabled(False)
        self.progressBar.setValue(0)
        t = threading.Thread(target=self.download_event)
        t.start()   
        self.downloadButton.setEnabled(True) 
        self.exitButton.setEnabled(True)
        self.songEdit.setEnabled(True)

    def exit_clicked(self):
        sys.exit()

    def about_clicked(self):
        webbrowser.open_new_tab("https://www.mastella.eu/")

    def info_clicked(self):
        webbrowser.open_new_tab("https://www.mastella.eu/YTMP3.html")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YTMP3"))
        self.songEdit.setPlainText(_translate("MainWindow", "First song\n"
"Second song\n"
"...."))
        self.toolButton.setText(_translate("MainWindow", "ABOUT"))
        self.downloadButton.setText(_translate("MainWindow", "DOWNLOAD"))
        self.infoButton.setText(_translate("MainWindow", "INFO"))
        self.exitButton.setText(_translate("MainWindow", "EXIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
