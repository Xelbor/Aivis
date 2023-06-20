from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWinExtras import QtWin
import keyboard
import win32gui
import win32con
import sys

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

top_windows = []

win32gui.EnumWindows(windowEnumerationHandler, top_windows)

for i, min in enumerate(top_windows):
    if min[1]:
        if "Aivis Soft" in min[1]:
            MessageBox = win32gui.MessageBox
            MessageBox(None, "Программа уже активна", "Предупреждение", win32con.MB_OK | win32con.MB_ICONWARNING)

            print(min, '<---- это приложение уже запущено ранее.')

            win32gui.ShowWindow(min[0], 5)
            win32gui.SetForegroundWindow(min[0])
            sys.exit()

            break

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 630)
        MainWindow.setFixedSize(1013, 630)

        myappid = 'mycompany.myproduct.subproduct.version'
        QtWin.setCurrentProcessExplicitAppUserModelID(myappid)

        MainWindow.setWindowIcon(QtGui.QIcon('Interface/Icon.ico'))

        MainWindow.setStyleSheet("background-image: url(Interface/Main2.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")

        # Убирания виндовс рамок
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.tray_icon = QIcon('Interface/Icon.ico')
        self.tray = QSystemTrayIcon(MainWindow)
        self.tray.setIcon(self.tray_icon)

        self.show_action = QAction("Открыть окно", MainWindow)
        self.show_action.triggered.connect(MainWindow.showNormal)

        self.exit_action = QAction("Выход", MainWindow)
        self.exit_action.triggered.connect(lambda: self.exit())

        self.tray_menu = QMenu(MainWindow)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.exit_action)
        self.tray_menu.setStyleSheet("color: white;")

        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # добавляем обработчики событий мыши
        self.draggable = True
        self.offset = None

        def mousePressEvent(event):
                if event.button() == QtCore.Qt.LeftButton:
                        self.offset = event.pos()
                        self.draggable = True
                        event.accept()

        def mouseMoveEvent(event):
                if self.draggable and self.offset is not None:
                        MainWindow.move(MainWindow.pos() + event.pos() - self.offset)
                        event.accept()

        def mouseReleaseEvent(event):
                if event.button() == QtCore.Qt.LeftButton:
                        self.draggable = False
                        event.accept()

        # подключаем обработчики к виджету
        self.centralwidget.mousePressEvent = mousePressEvent
        self.centralwidget.mouseMoveEvent = mouseMoveEvent
        self.centralwidget.mouseReleaseEvent = mouseReleaseEvent

        self.pushButton_close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(972, -1, 50, 21))
        self.pushButton_close.setStyleSheet("QPushButton {\n"
"    background-image: url(\"Interface/exit_programm.png\");\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-image: url(\"Interface/exit_programm_guidance.png\");\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}")
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.clicked.connect(MainWindow.close)

        def closeEvent(event):
                event.ignore()
                MainWindow.hide()
                self.tray.showMessage("Программа свернута в трей",
                                      "Нажмите правой кнопкой мыши на иконке для доступа к действиям")

        MainWindow.closeEvent = closeEvent

        self.pushButton_collapse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_collapse.setGeometry(QtCore.QRect(949, -4, 41, 31))
        self.pushButton_collapse.setStyleSheet("QPushButton {\n"
"    background-image: url(\"Interface/collapse.png\");\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-image: url(\"Interface/collapse_guidance .png\");\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}")

        self.pushButton_collapse.setText("")
        self.pushButton_collapse.setObjectName("pushButton_collapse")
        self.pushButton_collapse.clicked.connect(MainWindow.showMinimized)

        self.pushButton_options = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_options.setGeometry(QtCore.QRect(20, 130, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_options.setFont(font)
        self.pushButton_options.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_options.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")

        self.pushButton_options.setObjectName("pushButton_options")

        self.pushButton_options_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_options_home.setGeometry(QtCore.QRect(20, 130, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_options_home.setFont(font)
        self.pushButton_options_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_options_home.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")

        self.pushButton_options_home.setObjectName("pushButton_options")
        self.pushButton_options_home.hide()

        self.pushButton_commands = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_commands.setGeometry(QtCore.QRect(20, 178, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_commands.setFont(font)
        self.pushButton_commands.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_commands.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")
        self.pushButton_commands.setObjectName("pushButton_commands")

        self.pushButton_commands_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_commands_home.setGeometry(QtCore.QRect(20, 178, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_commands_home.setFont(font)
        self.pushButton_commands_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_commands_home.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")
        self.pushButton_commands_home.setObjectName("pushButton_commands_home")

        self.pushButton_communication = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_communication.setGeometry(QtCore.QRect(20, 220, 91, 31))

        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_communication.setFont(font)
        self.pushButton_communication.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_communication.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")
        self.pushButton_communication.setObjectName("pushButton_communication")

        self.pushButton_communication_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_communication_home.setGeometry(QtCore.QRect(20, 220, 91, 31))

        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_communication_home.setFont(font)
        self.pushButton_communication_home.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_communication_home.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid white;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")
        self.pushButton_communication_home.setObjectName("pushButton_home_communication")
        self.pushButton_communication_home.hide()

        self.widget_aivis_logo = QtWidgets.QWidget(self.centralwidget)
        self.widget_aivis_logo.setGeometry(QtCore.QRect(443, -27, 120, 80))
        self.widget_aivis_logo.setStyleSheet("background-image: url(Interface/Aivis_logo.png);\n"
"background-repeat: no-repeat;\n"
"background-position: center;")
        self.widget_aivis_logo.setObjectName("widget_aivis_logo")
        self.label_communication = QtWidgets.QLabel(self.centralwidget)
        self.label_communication.setGeometry(QtCore.QRect(154, 150, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.label_communication.setFont(font)
        self.label_communication.setStyleSheet("color: white;")
        self.label_communication.setObjectName("label_communication")
        self.label_communication.hide()
        self.label_Created = QtWidgets.QLabel(self.centralwidget)
        self.label_Created.setGeometry(QtCore.QRect(8, 0, 101, 21))
        self.label_Created.setStyleSheet("color: gray;")
        self.label_Created.setObjectName("label_Created")
        self.pushButton_mail_copy = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mail_copy.setGeometry(QtCore.QRect(170, 180, 151, 20))
        self.pushButton_mail_copy.hide()
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_mail_copy.setFont(font)
        self.pushButton_mail_copy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_mail_copy.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: gray;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid gray;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")

        self.pushButton_mail_copy.setObjectName("pushButto_mail_copy")
        self.pushButton_gmail_copy = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_gmail_copy.setGeometry(QtCore.QRect(170, 200, 181, 20))
        self.pushButton_gmail_copy.hide()
        font = QtGui.QFont()
        font.setFamily("Lucida Sans")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_gmail_copy.setFont(font)
        self.pushButton_gmail_copy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_gmail_copy.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: gray;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    border-bottom: 2px solid gray;\n"
"    position: relative;\n"
"    animation: slideIn 0.25s ease-in forwards;\n"
"}\n"
"\n"
"@keyframes slideIn {\n"
"    from {\n"
"        left: 0;\n"
"        width: 0;\n"
"    }\n"
"    to {\n"
"        left: 0;\n"
"        width: 100%;\n"
"    }\n"
"}\n"
"")
        self.pushButton_gmail_copy.setObjectName("pushButton_gmail_copy")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(600, 560, 411, 41))
        self.frame.setStyleSheet("background-image: url(Interface/copyed.png);\n"
                                 "background-repeat: no-repeat;\n"
                                 "background-position: center;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.hide()
        self.label_copyed = QtWidgets.QLabel(self.frame)
        self.label_copyed.setGeometry(QtCore.QRect(30, 10, 71, 21))
        self.label_copyed.setStyleSheet("color: white;")
        self.label_copyed.setObjectName("label")
        self.frame.hide()
        self.pushButton_exit_copyed = QtWidgets.QPushButton(self.frame)
        self.pushButton_exit_copyed.setGeometry(QtCore.QRect(380, 14, 21, 16))
        self.pushButton_exit_copyed.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_exit_copyed.setStyleSheet(
                "background-image: url(\"Interface/exit_programm.png\");\n"
                "background-repeat: no-repeat;\n"
                "background-position: center;\n"
                "background-color: transparent;\n"
                "color: white;\n"
                "")
        self.pushButton_exit_copyed.setText("")
        self.pushButton_exit_copyed.setObjectName("pushButton")
        self.pushButton_exit_copyed.hide()

        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(142, 130, 301, 16))
        self.label_name.setStyleSheet("color: white;")
        self.label_name.setObjectName("label_name")
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setGeometry(QtCore.QRect(160, 160, 113, 20))
        self.lineEdit_name.setStyleSheet("color: black;\n"
                                         "background: white;")
        self.lineEdit_name.setObjectName("lineEdit_name")

        self.label_aivis = QtWidgets.QLabel(self.centralwidget)
        self.label_aivis.setGeometry(QtCore.QRect(400, 450, 230, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_aivis.setFont(font)
        self.label_aivis.setStyleSheet("color: gray;")
        self.label_aivis.setText("")
        self.label_aivis.setObjectName("label_aivis")

        self.label_print_voice = QtWidgets.QLabel(self.centralwidget)
        self.label_print_voice.setGeometry(QtCore.QRect(376, 465, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.label_print_voice.setFont(font)
        self.label_print_voice.setStyleSheet("color: gray;")
        self.label_print_voice.setText("")
        self.label_print_voice.setObjectName("label_print_voice")
        self.label_hint_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_hint_1.setGeometry(QtCore.QRect(160, 182, 241, 20))
        self.label_hint_1.setStyleSheet("color: gray;")
        self.label_hint_1.setObjectName("label_hint_1")
        self.label_hint_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_hint_2.setGeometry(QtCore.QRect(160, 200, 241, 20))
        self.label_hint_2.setStyleSheet("color: gray;")
        self.label_hint_2.setObjectName("label_hint_2")
        self.label_hint_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_hint_3.setGeometry(QtCore.QRect(160, 218, 241, 20))
        self.label_hint_3.setStyleSheet("color: gray;")
        self.label_hint_3.setObjectName("label_hint_3")
        self.label_hint_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_hint_4.setGeometry(QtCore.QRect(160, 235, 241, 20))
        self.label_hint_4.setStyleSheet("color: gray;")
        self.label_hint_4.setObjectName("label_hint_4")
        self.comboBox_micro = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_micro.setGeometry(QtCore.QRect(160, 230, 151, 22))
        self.comboBox_micro.setStyleSheet("QComboBox QAbstractItemView {\n"
                                                    "  color: rgb(247, 249, 250);    \n"
                                                    "  background-color: #4f5154;\n"
                                                    "  selection-background-color: rgb(58, 61, 66);\n"
                                                    "}")
        self.comboBox_micro.setObjectName("comboBox_micro")

        self.label_logo_aivis = QtWidgets.QLabel(self.centralwidget)
        self.label_logo_aivis.setGeometry(QtCore.QRect(630, 160, 161, 111))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(38)
        font.setBold(True)
        font.setWeight(75)
        self.label_logo_aivis.setFont(font)
        self.label_logo_aivis.setStyleSheet("color: gray;")
        self.label_logo_aivis.setObjectName("label_logo_aivis")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(150, 100, 251, 411))
        self.scrollArea.setStyleSheet("background-color: white;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 249, 409))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 141, 411))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.listWidget.setStyleSheet("color:white;\n"
"background-color: black;")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.insertItem(0, "Погода")
        self.listWidget.insertItem(1, "Поиск на YouTube")
        self.listWidget.insertItem(2, "Поиск в Google")
        self.listWidget.insertItem(3, "Браузер")
        self.listWidget.insertItem(4, "Браузер с YouTube")
        self.listWidget.insertItem(5, "Открытие Программы")
        self.listWidget.insertItem(6, "Выключение ПК")
        self.listWidget.insertItem(7, "Перезагрузка ПК")
        self.listWidget.insertItem(8, "Сон")

        self.listWidget.itemClicked.connect(self.handleItemClicked)

        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 0, 111, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_on_off = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_on_off.setStyleSheet("color:white;")
        self.label_on_off.setObjectName("label_on_off")
        self.verticalLayout.addWidget(self.label_on_off)
        self.listWidget_2 = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget_2.setStyleSheet("color:white;\n"
"background-color: black;")
        self.listWidget_2.setObjectName("listWidget_2")

        self.listWidget_2.itemClicked.connect(self.handle_item_click)  # Добавлено self

        self.listWidget_2.insertItem(0, "Вкл")
        self.listWidget_2.insertItem(1, "Вкл")
        self.listWidget_2.insertItem(2, "Вкл")
        self.listWidget_2.insertItem(3, "Вкл")
        self.listWidget_2.insertItem(4, "Вкл")
        self.listWidget_2.insertItem(5, "Вкл")
        self.listWidget_2.insertItem(6, "Вкл")
        self.listWidget_2.insertItem(7, "Вкл")
        self.listWidget_2.insertItem(8, "Вкл")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 290, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: gray;")
        self.label_4.setObjectName("label_4")
        self.comboBox_city = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_city.setGeometry(QtCore.QRect(430, 150, 131, 22))
        self.comboBox_city.setStyleSheet("color: white;\n"
                                         "background-color: transparent;\n"
                                         "\n"
                                         "            QComboBox::drop-down {\n"
                                         "                width: 0px;\n"
                                         "            }\n"
                                         "            QComboBox::down-arrow {\n"
                                         "                image: url(\"Interface/ComboBox_arrow.png\");\n"
                                         "                width: 16px;\n"
                                         "                height: 16px;\n"
                                         "            }")
        self.comboBox_city.setObjectName("comboBox_city")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")

        self.checkBox_first_video = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_first_video.setGeometry(QtCore.QRect(450, 150, 251, 21))
        self.checkBox_first_video.setTabletTracking(False)
        self.checkBox_first_video.setStyleSheet("color: white;")
        self.checkBox_first_video.setChecked(True)
        self.checkBox_first_video.setObjectName("checkBox_first_video")

        self.checkBox_read_text = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_read_text.setEnabled(True)
        self.checkBox_read_text.setGeometry(QtCore.QRect(450, 211, 321, 21))
        self.checkBox_read_text.setTabletTracking(False)
        self.checkBox_read_text.setStyleSheet("color: white;")
        self.checkBox_read_text.setChecked(True)
        self.checkBox_read_text.setObjectName("checkBox_read_text")
        self.checkBox_open_results = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_open_results.setGeometry(QtCore.QRect(450, 181, 471, 21))
        self.checkBox_open_results.setTabletTracking(False)
        self.checkBox_open_results.setStyleSheet("color: white;")
        self.checkBox_open_results.setChecked(True)
        self.checkBox_open_results.setObjectName("checkBox_open_results")
        self.checkBox_open_first_result = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_open_first_result.setGeometry(QtCore.QRect(450, 155, 471, 21))
        self.checkBox_open_first_result.setTabletTracking(False)
        self.checkBox_open_first_result.setStyleSheet("color: white;")
        self.checkBox_open_first_result.setChecked(True)
        self.checkBox_open_first_result.setObjectName("checkBox_first_result")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(420, 150, 221, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_review = QtWidgets.QLabel(self.centralwidget)
        self.label_review.setGeometry(QtCore.QRect(420, 120, 177, 21))
        self.label_review.setStyleSheet("color: gray;")
        self.label_review.setObjectName("label_review")
        self.lineEdit_review = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_review.setObjectName("lineEdit_review")
        self.lineEdit_review.setStyleSheet("color: white;")
        self.horizontalLayout.addWidget(self.lineEdit_review)
        self.pushButton_review = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_review.setStyleSheet("QPushButton {\n"
                                      "    background-color: transparent;\n"
                                      "    color: white;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: white;\n"
                                      "    border: 2px solid white;\n"
                                      "    padding: 5px;\n"
                                      "     border-radius: 5px;\n"
                                      "}")
        self.pushButton_review.setObjectName("pushButton_review")
        self.horizontalLayout.addWidget(self.pushButton_review)
        self.pushButton_review.clicked.connect(self.openFileDialog)

        self.pushButton_key = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_key.setGeometry(QtCore.QRect(430, 170, 51, 31))
        self.pushButton_key.setStyleSheet("QPushButton {\n"
                                          "    background-color: transparent;\n"
                                          "    color: white;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: white;\n"
                                          "    border: 2px solid white;\n"
                                          "    padding: 5px;\n"
                                          "     border-radius: 5px;\n"
                                          "}")
        self.pushButton_key.setObjectName("pushButton_key")
        self.pushButton_key.clicked.connect(self.start_key_capture)

        self.is_key_capture_enabled = False
        self.captured_key = None

        self.label_key_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_key_1.setGeometry(QtCore.QRect(410, 110, 351, 21))
        self.label_key_1.setStyleSheet("color: gray;")
        self.label_key_1.setObjectName("label_key_1")
        self.label_key_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_key_2.setGeometry(QtCore.QRect(410, 133, 241, 21))
        self.label_key_2.setStyleSheet("color: gray;")
        self.label_key_2.setObjectName("label_key_2")
        self.label_key = QtWidgets.QLabel(self.centralwidget)
        self.label_key.setGeometry(QtCore.QRect(430, 220, 171, 21))
        self.label_key.setStyleSheet("color: gray;")
        self.label_key.setObjectName("label_key")

        self.label_notifications = QtWidgets.QLabel(self.centralwidget)
        self.label_notifications.setGeometry(QtCore.QRect(142, 260, 341, 16))
        self.label_notifications.setStyleSheet("color: white;")
        self.label_notifications.setObjectName("label_notifications")
        self.checkBox_notifications = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_notifications.setGeometry(QtCore.QRect(170, 290, 71, 17))
        self.checkBox_notifications.setStyleSheet("color: gray")
        self.checkBox_notifications.setChecked(True)
        self.checkBox_notifications.setObjectName("checkBox_notifications")

        self.key_callback = None

        self.label_notifications.hide()
        self.checkBox_notifications.hide()
        self.label_review.hide()
        self.pushButton_key.hide()
        self.label_key.hide()
        self.label_key_1.hide()
        self.label_key_2.hide()
        self.horizontalLayoutWidget.hide()
        self.pushButton_review.hide()
        self.lineEdit_review.hide()
        self.checkBox_open_results.hide()
        self.checkBox_read_text.hide()
        self.checkBox_open_first_result.hide()
        self.checkBox_first_video.hide()
        self.comboBox_city.hide()
        self.label_4.hide()
        self.pushButton_commands_home.hide()
        self.comboBox_micro.hide()
        self.listWidget.hide()
        self.listWidget_2.hide()
        self.scrollArea.hide()
        self.label_logo_aivis.hide()
        self.label_hint_1.hide()
        self.label_hint_2.hide()
        self.label_hint_3.hide()
        self.label_hint_4.hide()
        self.label_name.hide()
        self.lineEdit_name.hide()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        def reset_buttons_communication():
                self.pushButton_options.clicked.connect(self.pushButton_communication_home.hide)
                self.pushButton_options.clicked.connect(self.pushButton_communication.show)
                self.pushButton_options.clicked.connect(self.label_communication.hide)
                self.pushButton_options.clicked.connect(self.pushButton_mail_copy.hide)
                self.pushButton_options.clicked.connect(self.pushButton_gmail_copy.hide)

        def reset_buttons_options():
                self.pushButton_communication.clicked.connect(self.pushButton_options_home.hide)
                self.pushButton_communication.clicked.connect(self.pushButton_options.show)
                self.pushButton_communication.clicked.connect(self.label_name.hide)
                self.pushButton_communication.clicked.connect(self.lineEdit_name.hide)

        def exit_copyed():
                self.label_copyed.hide()
                self.frame.hide()
                self.pushButton_exit_copyed.hide()

        def copy_to_clipboard_mail():
                clipboard = QtWidgets.QApplication.clipboard()
                text = self.pushButton_mail_copy.text()
                text = text.replace("Mail:", "")
                clipboard.setText(text)
                self.label_copyed.show()
                self.frame.show()
                self.pushButton_exit_copyed.show()
                self.timer = QtCore.QTimer()
                self.timer.start(5000)
                self.timer.timeout.connect(exit_copyed)

        def copy_to_clipboard_gmail():
                clipboard = QtWidgets.QApplication.clipboard()
                text = self.pushButton_gmail_copy.text()
                text = text.replace("Gmail:", "")
                clipboard.setText(text)
                self.frame.show()
                self.label_copyed.show()
                self.pushButton_exit_copyed.show()
                self.timer = QtCore.QTimer()
                self.timer.start(5000)
                self.timer.timeout.connect(exit_copyed)

        self.pushButton_exit_copyed.clicked.connect(exit_copyed)

        self.pushButton_mail_copy.clicked.connect(copy_to_clipboard_mail)
        self.pushButton_gmail_copy.clicked.connect(copy_to_clipboard_gmail)

        def save_to_file(text):
                with open('name.txt', 'w') as f:
                        f.write(text.lower())  # Записываем текст из lineEdit_name в файл

        self.lineEdit_name.textChanged.connect(save_to_file)

        self.retranslateUi(MainWindow)
        self.pushButton_communication.clicked.connect(self.pushButton_mail_copy.show)
        self.pushButton_communication.clicked.connect(self.pushButton_gmail_copy.show)
        self.pushButton_communication.clicked.connect(self.label_communication.show)
        self.pushButton_communication.clicked.connect(self.pushButton_communication.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_communication_home.show)
        self.pushButton_communication.clicked.connect(self.label_hint_1.hide)
        self.pushButton_communication.clicked.connect(self.label_hint_2.hide)
        self.pushButton_communication.clicked.connect(self.label_hint_3.hide)
        self.pushButton_communication.clicked.connect(self.label_hint_4.hide)
        self.pushButton_communication.clicked.connect(self.label_print_voice.hide)
        self.pushButton_communication.clicked.connect(self.label_aivis.hide)
        self.pushButton_communication.clicked.connect(self.label_print_voice.hide)
        self.pushButton_communication.clicked.connect(self.label_aivis.hide)
        self.pushButton_communication.clicked.connect(self.listWidget.hide)
        self.pushButton_communication.clicked.connect(self.listWidget_2.hide)
        self.pushButton_communication.clicked.connect(self.comboBox_city.hide)
        self.pushButton_communication.clicked.connect(self.checkBox_first_video.hide)
        self.pushButton_communication.clicked.connect(self.checkBox_open_first_result.hide)
        self.pushButton_communication.clicked.connect(self.checkBox_open_results.hide)
        self.pushButton_communication.clicked.connect(self.checkBox_read_text.hide)
        self.pushButton_communication.clicked.connect(self.horizontalLayoutWidget.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_review.hide)
        self.pushButton_communication.clicked.connect(self.lineEdit_review.hide)
        self.pushButton_communication.clicked.connect(self.label_logo_aivis.hide)
        self.pushButton_communication.clicked.connect(self.label_4.hide)
        self.pushButton_communication.clicked.connect(self.scrollAreaWidgetContents_2.hide)
        self.pushButton_communication.clicked.connect(self.scrollArea.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_commands_home.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_commands.show)
        self.pushButton_communication.clicked.connect(self.label_review.hide)
        self.pushButton_communication.clicked.connect(self.label_key.hide)
        self.pushButton_communication.clicked.connect(self.label_key_1.hide)
        self.pushButton_communication.clicked.connect(self.label_key_2.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_key.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_options_home.hide)
        self.pushButton_communication.clicked.connect(self.label_name.hide)
        self.pushButton_communication.clicked.connect(self.lineEdit_name.hide)
        self.pushButton_communication.clicked.connect(self.pushButton_options.show)
        self.pushButton_communication.clicked.connect(self.label_notifications.hide)
        self.pushButton_communication.clicked.connect(self.checkBox_notifications.hide)
        self.pushButton_communication_home.clicked.connect(self.label_hint_1.hide)
        self.pushButton_communication_home.clicked.connect(self.label_hint_2.hide)
        self.pushButton_communication_home.clicked.connect(self.label_hint_3.hide)
        self.pushButton_communication_home.clicked.connect(self.label_hint_4.hide)
        self.pushButton_communication_home.clicked.connect(self.pushButton_communication_home.hide)
        self.pushButton_communication_home.clicked.connect(self.pushButton_communication.show)
        self.pushButton_communication_home.clicked.connect(self.label_communication.hide)
        self.pushButton_communication_home.clicked.connect(self.pushButton_mail_copy.hide)
        self.pushButton_communication_home.clicked.connect(self.pushButton_gmail_copy.hide)
        self.pushButton_communication_home.clicked.connect(self.label_print_voice.show)
        self.pushButton_communication_home.clicked.connect(self.label_aivis.show)
        self.pushButton_options.clicked.connect(self.label_name.show)
        self.pushButton_options.clicked.connect(self.lineEdit_name.show)
        self.pushButton_options.clicked.connect(self.label_hint_1.show)
        self.pushButton_options.clicked.connect(self.label_hint_2.show)
        self.pushButton_options.clicked.connect(self.label_hint_3.show)
        self.pushButton_options.clicked.connect(self.label_hint_4.show)
        self.pushButton_options.clicked.connect(self.pushButton_options_home.show)
        self.pushButton_options.clicked.connect(self.label_print_voice.hide)
        self.pushButton_options.clicked.connect(self.label_aivis.hide)
        self.pushButton_options.clicked.connect(self.listWidget.hide)
        self.pushButton_options.clicked.connect(self.listWidget_2.hide)
        self.pushButton_options.clicked.connect(self.comboBox_city.hide)
        self.pushButton_options.clicked.connect(self.checkBox_first_video.hide)
        self.pushButton_options.clicked.connect(self.checkBox_open_first_result.hide)
        self.pushButton_options.clicked.connect(self.checkBox_open_results.hide)
        self.pushButton_options.clicked.connect(self.checkBox_read_text.hide)
        self.pushButton_options.clicked.connect(self.horizontalLayoutWidget.hide)
        self.pushButton_options.clicked.connect(self.pushButton_review.hide)
        self.pushButton_options.clicked.connect(self.lineEdit_review.hide)
        self.pushButton_options.clicked.connect(self.label_logo_aivis.hide)
        self.pushButton_options.clicked.connect(self.label_4.hide)
        self.pushButton_options.clicked.connect(self.scrollAreaWidgetContents_2.hide)
        self.pushButton_options.clicked.connect(self.scrollArea.hide)
        self.pushButton_options.clicked.connect(self.pushButton_commands_home.hide)
        self.pushButton_options.clicked.connect(self.pushButton_commands.show)
        self.pushButton_options.clicked.connect(self.label_review.hide)
        self.pushButton_options.clicked.connect(self.label_key.hide)
        self.pushButton_options.clicked.connect(self.label_key_1.hide)
        self.pushButton_options.clicked.connect(self.label_key_2.hide)
        self.pushButton_options.clicked.connect(self.pushButton_key.hide)
        self.pushButton_options.clicked.connect(self.label_notifications.show)
        self.pushButton_options.clicked.connect(self.checkBox_notifications.show)
        self.pushButton_options.clicked.connect(self.pushButton_mail_copy.hide)
        self.pushButton_options.clicked.connect(self.pushButton_gmail_copy.hide)
        self.pushButton_options.clicked.connect(self.label_communication.hide)
        self.pushButton_options_home.clicked.connect(self.label_name.hide)
        self.pushButton_options_home.clicked.connect(self.lineEdit_name.hide)
        self.pushButton_options_home.clicked.connect(self.pushButton_options_home.hide)
        self.pushButton_options_home.clicked.connect(self.label_hint_1.hide)
        self.pushButton_options_home.clicked.connect(self.label_hint_2.hide)
        self.pushButton_options_home.clicked.connect(self.label_hint_3.hide)
        self.pushButton_options_home.clicked.connect(self.label_hint_4.hide)
        self.pushButton_options_home.clicked.connect(self.pushButton_options.show)
        self.pushButton_options_home.clicked.connect(reset_buttons_communication)
        self.pushButton_options_home.clicked.connect(self.label_print_voice.show)
        self.pushButton_options_home.clicked.connect(self.label_aivis.show)
        self.pushButton_options_home.clicked.connect(self.label_notifications.hide)
        self.pushButton_options_home.clicked.connect(self.checkBox_notifications.hide)
        self.pushButton_communication.clicked.connect(reset_buttons_options)
        self.pushButton_commands.clicked.connect(self.listWidget.show)
        self.pushButton_commands.clicked.connect(self.listWidget_2.show)
        self.pushButton_commands.clicked.connect(self.scrollArea.show)
        self.pushButton_commands.clicked.connect(self.label_on_off.show)
        self.pushButton_commands.clicked.connect(self.label_logo_aivis.show)
        self.pushButton_commands.clicked.connect(self.label_aivis.hide)
        self.pushButton_commands.clicked.connect(self.label_print_voice.hide)
        self.pushButton_commands.clicked.connect(self.label_4.show)
        self.pushButton_commands.clicked.connect(self.pushButton_commands_home.show)
        self.pushButton_commands.clicked.connect(self.scrollAreaWidgetContents_2.show)
        self.pushButton_commands.clicked.connect(self.scrollArea.show)
        self.pushButton_commands.clicked.connect(self.pushButton_options_home.hide)
        self.pushButton_commands.clicked.connect(self.label_name.hide)
        self.pushButton_commands.clicked.connect(self.lineEdit_name.hide)
        self.pushButton_commands.clicked.connect(self.label_print_voice.hide)
        self.pushButton_commands.clicked.connect(self.label_aivis.hide)
        self.pushButton_commands.clicked.connect(self.label_hint_1.hide)
        self.pushButton_commands.clicked.connect(self.label_hint_2.hide)
        self.pushButton_commands.clicked.connect(self.label_hint_3.hide)
        self.pushButton_commands.clicked.connect(self.label_hint_4.hide)
        self.pushButton_commands.clicked.connect(self.label_notifications.hide)
        self.pushButton_commands.clicked.connect(self.checkBox_notifications.hide)
        self.pushButton_commands_home.clicked.connect(self.listWidget.hide)
        self.pushButton_commands_home.clicked.connect(self.listWidget_2.hide)
        self.pushButton_commands_home.clicked.connect(self.scrollArea.hide)
        self.pushButton_commands_home.clicked.connect(self.label_on_off.hide)
        self.pushButton_commands_home.clicked.connect(self.label_logo_aivis.hide)
        self.pushButton_commands_home.clicked.connect(self.label_aivis.show)
        self.pushButton_commands_home.clicked.connect(self.label_print_voice.show)
        self.pushButton_commands_home.clicked.connect(self.label_4.hide)
        self.pushButton_commands_home.clicked.connect(self.pushButton_commands_home.hide)
        self.pushButton_commands_home.clicked.connect(self.comboBox_city.hide)
        self.pushButton_commands_home.clicked.connect(self.checkBox_first_video.hide)
        self.pushButton_commands_home.clicked.connect(self.checkBox_open_first_result.hide)
        self.pushButton_commands_home.clicked.connect(self.checkBox_open_results.hide)
        self.pushButton_commands_home.clicked.connect(self.checkBox_read_text.hide)
        self.pushButton_commands_home.clicked.connect(self.horizontalLayoutWidget.hide)
        self.pushButton_commands_home.clicked.connect(self.pushButton_review.hide)
        self.pushButton_commands_home.clicked.connect(self.lineEdit_review.hide)
        self.pushButton_commands_home.clicked.connect(self.label_review.hide)
        self.pushButton_commands_home.clicked.connect(self.label_key.hide)
        self.pushButton_commands_home.clicked.connect(self.label_key_1.hide)
        self.pushButton_commands_home.clicked.connect(self.label_key_2.hide)
        self.pushButton_commands_home.clicked.connect(self.pushButton_key.hide)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        with open('name.txt', 'r') as r:
                name = r.read()
                name = name.replace("'", "")

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aivis Soft"))
        self.pushButton_options.setText(_translate("MainWindow", " НАСТРОЙКИ"))
        self.pushButton_commands.setText(_translate("MainWindow", "КОМАНДЫ"))
        self.pushButton_commands_home.setText(_translate("MainWindow", "ГЛАВНАЯ"))
        self.pushButton_communication.setText(_translate("MainWindow", "СВЯЗЬ"))
        self.pushButton_communication_home.setText(_translate("MainWindow", "ГЛАВНАЯ"))
        self.label_communication.setText(_translate("MainWindow", "Связь с разработчиком:"))
        self.label_Created.setText(_translate("MainWindow", "Created by Xelbor"))
        self.pushButton_mail_copy.setText(_translate("MainWindow", "Mail: aivis.help@mail.ru"))
        self.pushButton_gmail_copy.setText(_translate("MainWindow", "Gmail: aivis.help@gmail.com"))
        self.label_copyed.setText(_translate("MainWindow", "Скопировано"))
        self.pushButton_options_home.setText(_translate("MainWindow", "ГЛАВНАЯ"))
        self.label_name.setText(_translate("MainWindow", "Выбор имени ассистента, разделяйте имя через запятую:"))
        self.lineEdit_name.setText(_translate("MainWindow", name))
        self.label_print_voice.setText(_translate("MainWindow", "loading"))
        self.label_hint_1.setText(_translate("MainWindow", "Выбирайте имя для ассистента так, чтобы оно"))
        self.label_hint_2.setText(_translate("MainWindow", "хорошо распознавалось. Это можно проверить"))
        self.label_hint_3.setText(_translate("MainWindow", "на вкладке \"Главная\". Нельзя в имени ставить"))
        self.label_hint_4.setText(_translate("MainWindow", "пробел."))
        self.label_4.setText(_translate("MainWindow", "Выберите функцию которую хотите настроить"))
        self.label.setText(_translate("MainWindow", " Функции"))
        self.label_logo_aivis.setText("AIVIS")
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Погода"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Поиск на YouTube"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Поиск в Google"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Браузер"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "Браузер с YouTube"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "Открытие Программы"))
        item = self.listWidget.item(6)
        item.setText(_translate("MainWindow", "Выключение ПК"))
        item = self.listWidget.item(7)
        item.setText(_translate("MainWindow", "Перезагрузка ПК"))
        item = self.listWidget.item(8)
        item.setText(_translate("MainWindow", "Сон"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.label_on_off.setText(_translate("MainWindow", " Вкл/Выкл Функций"))
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.comboBox_city.setItemText(0, _translate("MainWindow", "Москва"))
        self.comboBox_city.setItemText(1, _translate("MainWindow", "Санкт-Петербург"))
        self.comboBox_city.setItemText(2, _translate("MainWindow", "Новосибирск"))
        self.comboBox_city.setItemText(3, _translate("MainWindow", "Екатеринбург"))
        self.comboBox_city.setItemText(4, _translate("MainWindow", "Нижний Новгород"))
        self.comboBox_city.setItemText(5, _translate("MainWindow", "Казань"))
        self.comboBox_city.setItemText(6, _translate("MainWindow", "Челябинск"))
        self.comboBox_city.setItemText(7, _translate("MainWindow", "Омск"))
        self.comboBox_city.setItemText(8, _translate("MainWindow", "Самара"))
        self.comboBox_city.setItemText(9, _translate("MainWindow", "Ростов-на-Дону"))
        self.comboBox_city.setItemText(10, _translate("MainWindow", "Курган"))
        self.comboBox_city.setItemText(11, _translate("MainWindow", "Владивосток"))
        self.comboBox_city.setItemText(12, _translate("MainWindow", "Красноярск"))
        self.comboBox_city.setItemText(13, _translate("MainWindow", "Пермь"))
        self.comboBox_city.setItemText(14, _translate("MainWindow", "Уфа"))
        self.checkBox_first_video.setText(_translate("MainWindow", "Открывать ли первое по результатам видео"))
        self.checkBox_read_text.setText(_translate("MainWindow", "Включение/выключение читания текста по запросу в гугл "))
        self.checkBox_open_results.setText(_translate("MainWindow", "Окрывать вкладку с результатами"))
        self.checkBox_open_first_result.setText(_translate("MainWindow", "Окрывать вкладку с первым результатом"))
        self.pushButton_review.setText(_translate("MainWindow", "Обзор"))
        self.label_review.setText(_translate("MainWindow", "Выберите путь к вашей программе"))
        self.pushButton_key.setText(_translate("MainWindow", "\\"))
        self.label_key_1.setText(_translate("MainWindow", "Нажмите на кнопку а потом на клавишу чтобы установить клавишу "))
        self.label_key_2.setText(_translate("MainWindow", "при нажатии которой ассистент выйдет из сна"))
        self.label_key.setText(_translate("MainWindow", "Нажмите на любую клавишу"))
        self.label_notifications.setText(_translate("MainWindow", "Хотите ли вы чтобы вам приходло уведомление об обновлениях?"))
        self.checkBox_notifications.setText(_translate("MainWindow", "Включено"))

    def handleItemClicked(self, item):
        if self.listWidget.row(item) == 0:
                self.label_review.hide()
                self.label_key_1.hide()
                self.label_key_2.hide()
                self.pushButton_key.hide()
                self.horizontalLayoutWidget.hide()
                self.pushButton_review.hide()
                self.lineEdit_review.hide()
                self.comboBox_city.show()
                self.checkBox_first_video.hide()
                self.checkBox_open_first_result.hide()
                self.checkBox_open_results.hide()
                self.checkBox_read_text.hide()
                self.label_4.hide()
                self.label_logo_aivis.hide()
        if self.listWidget.row(item) == 1:
                self.label_review.hide()
                self.label_key_1.hide()
                self.label_key_2.hide()
                self.pushButton_key.hide()
                self.horizontalLayoutWidget.hide()
                self.pushButton_review.hide()
                self.lineEdit_review.hide()
                self.checkBox_first_video.show()
                self.comboBox_city.hide()
                self.checkBox_open_first_result.hide()
                self.checkBox_open_results.hide()
                self.checkBox_read_text.hide()
                self.horizontalLayoutWidget.hide()
                self.pushButton_review.hide()
                self.lineEdit_review.hide()
                self.label_4.hide()
                self.label_logo_aivis.hide()
        if self.listWidget.row(item) == 2:
                self.label_review.hide()
                self.label_key_1.hide()
                self.label_key_2.hide()
                self.pushButton_key.hide()
                self.checkBox_open_first_result.show()
                self.checkBox_open_results.show()
                self.checkBox_read_text.show()
                self.checkBox_first_video.hide()
                self.comboBox_city.hide()
                self.horizontalLayoutWidget.hide()
                self.pushButton_review.hide()
                self.lineEdit_review.hide()
                self.label_4.hide()
                self.label_logo_aivis.hide()
        if self.listWidget.row(item) == 5:
                self.label_review.show()
                self.label_key_1.hide()
                self.label_key_2.hide()
                self.pushButton_key.hide()
                self.horizontalLayoutWidget.show()
                self.pushButton_review.show()
                self.lineEdit_review.show()
                self.checkBox_open_first_result.hide()
                self.checkBox_open_results.hide()
                self.checkBox_read_text.hide()
                self.checkBox_first_video.hide()
                self.comboBox_city.hide()
                self.label_4.hide()
                self.label_logo_aivis.hide()
        if self.listWidget.row(item) == 8:
                self.label_review.hide()
                self.label_key_1.show()
                self.label_key_2.show()
                self.pushButton_key.show()
                self.horizontalLayoutWidget.hide()
                self.pushButton_review.hide()
                self.lineEdit_review.hide()
                self.checkBox_open_first_result.hide()
                self.checkBox_open_results.hide()
                self.checkBox_read_text.hide()
                self.checkBox_first_video.hide()
                self.comboBox_city.hide()
                self.label_4.hide()
                self.label_logo_aivis.hide()

    def handle_item_click(self, item):
            if item.text() == "Вкл":
                    item.setText("Выкл")
            elif item.text() == "Выкл":
                    item.setText("Вкл")

    def openFileDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None, "Выберите программу", "", "Исполняемые файлы (*.exe)",
                                                      options=options)
            if fileName:
                    self.lineEdit_review.setText(fileName)

    def start_key_capture(self):
            if not self.is_key_capture_enabled:
                    self.is_key_capture_enabled = True
                    self.label_key.show()

                    keyboard.on_press(self.handle_key_press)

    def handle_key_press(self, event):
            if self.is_key_capture_enabled:
                    self.captured_key = event.name
                    self.stop_key_capture()

    def stop_key_capture(self):
            self.is_key_capture_enabled = False

            if self.captured_key is not None:
                    self.pushButton_key.setText(self.captured_key)
                    self.label_key.hide()

    def reset_key_capture(self):
            self.is_key_capture_enabled = False
            self.captured_key = None
            self.pushButton_key.setText("Выбрать клавишу")