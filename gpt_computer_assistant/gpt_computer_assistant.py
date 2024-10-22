try:
    from .agent.chat_history import *
    from .agent.assistant import *
    from .llm import *
    from .llm_settings import llm_settings
    from .agent.agent import *
    from .agent.background import *

    from .gui.signal import *
    from .gui.button import *
    from .gui.settings import settings_popup
    from .gui.llmsettings import llmsettings_popup
    from .utils.db import *
    from .utils.telemetry import my_tracer, os_name

    from .audio.wake_word import wake_word
    from .audio.tts import text_to_speech
    from .character import name, developer

except ImportError:
    # This is for running the script directly
    # in order to test the GUI without rebuilding the package
    from agent.chat_history import *
    from agent.assistant import *
    from llm import *
    from llm_settings import llm_settings
    from agent.agent import *
    from agent.background import *
    from utils.db import *
    from gui.signal import *
    from gui.button import *
    from gui.settings import settings_popup
    from gui.llmsettings import llmsettings_popup
    from utils.telemetry import my_tracer, os_name
    from audio.wake_word import wake_word
    from audio.tts import text_to_speech
import platform
import threading
import time
import random
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QHBoxLayout,
)
from PyQt5.QtCore import QPoint

from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
import pygame


print("Imported all libraries")


from PyQt5 import QtCore


try:
    import ctypes

    myappid = "onuratakan.gpt_computer_assistant.gui.1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

the_input_box = None
the_input_text = None


the_input_box_pre = None


the_main_window = None


user_id = load_user_id()
os_name_ = os_name()



readed_sentences = []

import re
def split_with_multiple_delimiters(text, delimiters):
    """
    Splits the text by any of the given delimiters while keeping the delimiters in the resulting parts.

    :param text: The input text to be split.
    :param delimiters: A string of delimiters to split the text on.
    :return: A list of parts including the delimiters.
    """
    # Create a regular expression pattern that matches any of the delimiters
    pattern = re.compile(f'(.*?[{re.escape(delimiters)}])')
    parts = pattern.findall(text)

    # Check if the last part is not complete and remove it if necessary
    if (
        parts and text
        and not any(text.endswith(d) for d in delimiters)
        and parts
        and not any(parts[-1].endswith(d) for d in delimiters)
    ):
        parts.pop()

    return parts



def click_sound():
    pygame.mixer.init()


    retro = pygame.mixer.Sound(click_sound_path)
    retro.set_volume(0.1)
    retro.play()



class Worker(QThread):
    text_to_set = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.the_input_text = None
        self.make_animation = True
        self.commited_text = []

    def run(self):
        while True:
            self.msleep(500)  # Simulate a time-consuming task

            if self.the_input_text:
                last_text = self.commited_text[-1] if len(self.commited_text) > 0 else ""
                if self.the_input_text != last_text:
                    self.commited_text.append(self.the_input_text)

                    if len(self.the_input_text) > 90 or MainWindow.api_enabled or not self.make_animation:
                        self.text_to_set.emit(self.the_input_text)
                    else:
                        for i in range(len(self.the_input_text)):
                            self.text_to_set.emit(self.the_input_text[:i + 1])
                            self.msleep(10)





return_key_event = None
class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CustomTextEdit, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            global return_key_event
            return_key_event()
        super(CustomTextEdit, self).keyPressEvent(event)  # Process other key events normally




class Worker_2(QThread):
    text_to_set = pyqtSignal(str)
    text_to_set_title_bar = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.the_input_text = None
        self.title_bar_text = None
        self.prev = None
        self.commited_text = []

    def run(self):
        while True:
            self.msleep(500)  # Simulate a time-consuming task

            if self.the_input_text and (self.prev is None or self.prev != self.the_input_text):
                self.prev = self.the_input_text
                self.text_to_set.emit("True")
                for i in range(len(self.title_bar_text)):
                    self.text_to_set_title_bar.emit(self.title_bar_text[:i + 1])
                    self.msleep(10)    

            if not self.the_input_text and self.prev != self.the_input_text:
                self.prev = self.the_input_text
                self.text_to_set.emit("False")

                the_text = "  "+ name()

                for i in range(len(the_text)):
                    self.text_to_set_title_bar.emit(the_text[:i + 1])
                    self.msleep(10)                



class Worker_3(QThread):
    text_to_set = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.the_input_text = None



    def run(self):
        while True:
            self.msleep(500)  # Simulate a time-consuming task

            if self.the_input_text:
                self.text_to_set.emit("True")
                self.the_input_text = None




class Worker_collapse(QThread):
    text_to_set = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.the_input_text = None



    def run(self):
        while True:
            self.msleep(500)  # Simulate a time-consuming task

            if self.the_input_text:
                self.text_to_set.emit("True")
                self.the_input_text = None
               
        

class Worker_uncollapse(QThread):
    text_to_set = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.the_input_text = None



    def run(self):
        while True:
            self.msleep(500)  # Simulate a time-consuming task

            if self.the_input_text:
                self.text_to_set.emit("True")
                self.the_input_text = None
               


class DrawingWidget(QWidget):
    def __init__(self, parent=None):
        super(DrawingWidget, self).__init__(parent)
        # Set widget properties if needed, e.g., size

        self.main_ = parent
        self.active_button = ""

    def paintEvent(self, event):

        if llm_settings[load_model_settings()]["vision"] is True:
            self.main_.screen_available = True
        else:
            self.main_.screen_available = False



        self.main_.setAutoFillBackground(True)
        painter = QPainter(self)
        painter = painter

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#000"), 1))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        center_x = 95
        center_y = 40

        if "talking" in self.main_.state:
            # Draw a pulsating circle with smooth easing animation
            radius_variation = 5 * (1 + math.sin(self.main_.pulse_frame * math.pi / 100))
            radius = 70 + radius_variation
            painter.drawEllipse(
                int(center_x - radius / 2),
                int(center_y - radius / 2),
                int(radius),
                int(radius),
            )
        elif self.main_.state == "thinking":
            # more slow pulsating circle with smooth easing animation
            radius_variation = 5 * (1 + math.sin(self.main_.pulse_frame * math.pi / 100))
            radius = 70 + radius_variation
            painter.drawEllipse(
                int(center_x - radius / 2),
                int(center_y - radius / 2),
                int(radius),
                int(radius),
            )

        else:
            radius = 70
            if self.main_.screen_available:
                painter.drawEllipse( # Main Button
                    int(center_x - radius / 2),
                    int(center_y - radius / 2),
                    int(radius),
                    int(radius),
                )


        
        self.main_.circle_rect = QRect(
            int(center_x - radius / 2),
            int(center_y - radius / 2),
            int(radius),
            int(radius),
        )



        if not self.main_.state == "thinking":
            painter.setPen(QPen(QColor("#01EE8A"), 1)) 
            if self.main_.screen_available:
                painter.drawEllipse( # Main BUtton Green Border
                    int(center_x - radius / 2),
                    int(center_y - radius / 2),
                    int(radius),
                    int(radius),
                )
        else:
            painter.setPen(QPen(QColor("#23538F"), 1))
            
            painter.drawEllipse(
                int(center_x - radius / 2),
                int(center_y - radius / 2),
                int(radius),
                int(radius),
            )



        painter.setPen(QPen(QColor("#000"), 1))

       

        small_center_x = 165
        small_center_y = 25
        small_radius = 30
        
        painter.drawEllipse( # Microphone bacground black
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        self.main_.small_circle_rect = QRect(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        # Draw the icon inside the circle
        icon_size = small_radius * 2 // 3  # Adjust the icon size relative to the circle
        icon_rect = QRect(
            small_center_x - icon_size // 2,
            small_center_y - icon_size // 2,
            icon_size,
            icon_size,
        )
        self.main_.small_circle_recticon = QIcon(microphone_icon_path)
        self.main_.small_circle_recticon.paint(painter, icon_rect)


        small_center_x = 30
        small_center_y = 60
        small_radius = 30
        painter.drawEllipse(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        self.main_.small_circle_left = QRect(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        # Draw the icon inside the circle
        icon_size = small_radius * 2 // 3  # Adjust the icon size relative to the circle
        icon_rect = QRect(
            small_center_x - icon_size // 2,
            small_center_y - icon_size // 2,
            icon_size,
            icon_size,
        )
        self.main_.small_circle_lefticon = QIcon(audio_icon_path)
        self.main_.small_circle_lefticon.paint(painter, icon_rect)



        small_center_x = 30
        small_center_y = 25
        small_radius = 30
        if self.main_.screen_available:
            painter.drawEllipse( # ScreenShot BUtton
                int(small_center_x - small_radius / 2),
                int(small_center_y - small_radius / 2),
                int(small_radius),
                int(small_radius),
            )

        
        self.main_.small_circle_left_top = QRect(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )



        self.main_.screenshot_button_coordinates_size = [
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        ]

        if self.active_button == "screenshot":
            self.screenshot_button_border_activate(painter)
            self.active_button = ""


        if self.main_.screen_available:
            # Draw the icon inside the circle
            icon_size = small_radius * 2 // 3  # Adjust the icon size relative to the circle
            icon_rect = QRect(
                small_center_x - icon_size // 2,
                small_center_y - icon_size // 2,
                icon_size,
                icon_size,
            )
            self.main_.small_circle_left_topticon = QIcon(screenshot_icon_path)
            self.main_.small_circle_left_topticon.paint(painter, icon_rect)






        small_center_x = 165
        small_center_y = 60
        small_radius = 30
        painter.drawEllipse(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        self.main_.small_circle_collapse = QRect(
            int(small_center_x - small_radius / 2),
            int(small_center_y - small_radius / 2),
            int(small_radius),
            int(small_radius),
        )

        # Draw the icon inside the circle
        icon_size = small_radius * 2 // 3  # Adjust the icon size relative to the circle
        icon_rect = QRect(
            small_center_x - icon_size // 2,
            small_center_y - icon_size // 2,
            icon_size,
            icon_size,
        )

        if self.main_.collapse:
            self.main_.small_circle_collapse_icon = QIcon(down_icon_path)
        else:
            self.main_.small_circle_collapse_icon = QIcon(up_icon_path)
        self.main_.small_circle_collapse_icon.paint(painter, icon_rect)


    def screenshot_button_border_activate(self, painter):
        # Add an white border to the circle
        painter.setPen(QPen(QColor("#FFF"), 1))
        # Draw the ellipse with the specified green border
        self.main_.screenshot_button_border = painter.drawEllipse(
            self.main_.screenshot_button_coordinates_size[0],
            self.main_.screenshot_button_coordinates_size[1],
            self.main_.screenshot_button_coordinates_size[2],
            self.main_.screenshot_button_coordinates_size[3],
        )
        painter.setPen(QPen(QColor("#000"), 1)) 




    def mousePressEvent(self, event: QMouseEvent):


        self.main_.old_position = event.globalPos()

        with my_tracer.start_span("mouse_press_event") as span:
            span.set_attribute("user_id", user_id)
            span.set_attribute("os_name", os_name_)
            if self.main_.state == "idle" or "talking" in self.main_.state:
                try:
                    if self.main_.circle_rect.contains(event.pos()):

                        if self.main_.state == "aitalking":
                            self.main_.stop_ai_talking()

                        else:
                            self.main_.screenshot_and_microphone_button_action()
                except:
                    traceback.print_exc()

                try:
                            if self.main_.small_circle_rect.contains(event.pos()):
                                if self.main_.state == "aitalking":
                                    self.main_.stop_ai_talking()

                                else: 
                                    click_sound()
                                    self.main_.button_handler.toggle_recording(no_screenshot=True)
                except:
                    traceback.print_exc()

                try:

                            if self.main_.small_circle_left.contains(event.pos()):
                                if self.main_.state == "aitalking":
                                    self.main_.stop_ai_talking()

                                else:       
                                    click_sound()                          
                                    self.main_.button_handler.toggle_recording(take_system_audio=True)
                except:
                    traceback.print_exc()

                try:

                            if self.main_.small_circle_left_top.contains(event.pos()):
                                if self.main_.state == "aitalking":
                                    self.main_.stop_ai_talking()

                                else:
                                    click_sound()
                                    self.active_button = "screenshot"
                                    self.update()
                                    self.main_.button_handler.just_screenshot()
                except:
                    traceback.print_exc()

            try:
                if self.main_.small_circle_collapse.contains(event.pos()):
                    if self.main_.collapse:
                        self.main_.uncollapse_gca()
                    else:
                        self.main_.collapse_gca()


                    self.main_.update()
            except:
                pass


from PyQt5.QtCore import QVariantAnimation

class MainWindow(QMainWindow):
    api_enabled = False


    def screenshot_and_microphone_button_action(self):
        click_sound()
        if llm_settings[load_model_settings()]["vision"] is True:

            self.button_handler.toggle_recording(dont_save_image=True)
        else:
            self.button_handler.toggle_recording(no_screenshot=True)

    def stop_ai_talking(self):
        self.manuel_stop = True
        self.stop_talking = True

    def __init__(self):
        super().__init__()

        self.background_color = "45, 45, 45"
        self.opacity = 250
        self.border_radius = 10


        print("API Enabled:", MainWindow.api_enabled)
        if MainWindow.api_enabled:
            try:
                from .api import start_api
                start_api()
            except:
                raise Exception("API could not be started, please install gpt-computer-assistant[api]")
        self.stop_talking = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Remove the default title bar

        # Load the San Francisco font
        print("Loading font")
        print(font_dir)
        try:
            font_id = QtGui.QFontDatabase.addApplicationFont(font_dir)


            font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QtGui.QFont(font_family))
        except:
            print("Error loading font")


        self.state = "idle"
        self.pulse_timer = None

        self.button_handler = ButtonHandler(self)
        self.initUI()
        self.old_position = self.pos()





        self.collapse = is_collapse_setting_active()
        if self.collapse:
            self.collapse_window()

        global the_main_window
        the_main_window = self


        self.general_styling()

        if is_dark_mode_active():
            self.dark_mode()
        else:
            self.light_mode()


        self.wake_word_thread = None

        self.wake_word_active = False

        if load_pvporcupine_api_key() != "CHANGE_ME" and is_wake_word_active():
            self.wake_word_active = True
            self.wake_word_trigger()    


        self.manuel_stop = False    


        self.border_animation = None

        self.complated_answer = False


        self.reading_thread = False
        self.reading_thread_2 = False



    def init_border_animation(self):
        # Create a QVariantAnimation to handle color change
        border_animation = QVariantAnimation(
            self,
            valueChanged=self.update_border_color,
            startValue=QColor("#303030"),
            endValue=QColor("#23538F"),
            duration=2000  # Duration for one loop in milliseconds
        )
        border_animation.setLoopCount(-1)  # Loop indefinitely
        return border_animation

    def start_border_animation(self, status):
        print("FUNCTION TRİGGERED")
        if self.border_animation is None:
            self.border_animation = self.init_border_animation()

        status = status.lower() == "true"
        if status:
            self.border_animation.start()
        else:
            self.border_animation.stop()
            self.title_bar.setStyleSheet("background-color: #2E2E2E; color: white; border-style: solid; border-radius: 15px; border-width: 0px; color: #fff;")



    def update_border_color(self, color):
        self.title_bar.setStyleSheet(f"background-color: #2E2E2E; color: white; border-style: solid; border-radius: 15px; border-width: 2px; border-color: {color.name()}; color: #fff;")
        self.title_bar.setStyleSheet(f"background-color: #2E2E2E; color: white; border-style: solid; border-radius: 15px; border-width: 1px; border-color: {color.name()}; color: #fff;")

    # Existing methods...

    def general_styling(self, a=None):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(f"border-radius: {self.border_radius}px; background-color: rgba({self.background_color}, {self.opacity});")
        self.central_widget.setStyleSheet("border-style: solid; border-width: 1px; border-color: rgb(0,0,0,0);")

        self.input_box_style = "border-radius: 10px; border-bottom: 1px solid #01EE8A;"



        self.settingsButton_style = "border-radius: 5px; height: 25px; border-style: solid;"
        self.llmsettingsButton_style = "border-radius: 5px; height: 25px; border-style: solid;"

        self.btn_minimize.setStyleSheet("background-color: #2E2E2E; color: white; border-style: none;")
        self.btn_close.setStyleSheet("background-color: #2E2E2E; color: white; border-style: none;")


    def set_background_color(self, color):
        self.background_color = color
        self.worker_3.the_input_text = "True"

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.worker_3.the_input_text = "True"

    def set_border_radius(self, radius):
        self.border_radius = radius
        self.worker_3.the_input_text = "True"


    def wake_word_trigger(self):
        self.wake_word_thread = threading.Thread(target=self.wake_word)
        self.wake_word_thread.start()       

    def wake_word(self):
        from .agent.process import tts_if_you_can
        while True and is_wake_word_active() and self.wake_word_active:
            if wake_word(self):

                def random_accept_words():
                    return random.choice(["Yes", "Sir", "Boss", "Master"])


                tts_if_you_can(random_accept_words(), not_threaded=True)


                def trigger_wake_word():
                    if is_wake_word_screen_setting_active() and llm_settings[load_model_settings()]["vision"]:
                        self.button_handler.toggle_recording(dont_save_image=True)
                    else:
                        self.button_handler.toggle_recording(no_screenshot=True)

                if self.state == "aitalking":
                    self.manuel_stop = True
                    self.stop_talking = True
                    time.sleep(1)
                    trigger_wake_word()
                    print("Stop talking")
                else:
                    trigger_wake_word()







    def dark_mode(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#171717"))  # Set background color to white
        self.setPalette(p)
        self.input_box.setStyleSheet(self.input_box_style+"background-color: #2E2E2E; color: white;")



        self.settingsButton.setStyleSheet(self.settingsButton_style+"background-color: #2E2E2E; color: white;")
        self.llmsettingsButton.setStyleSheet(self.llmsettingsButton_style+"background-color: #2E2E2E; color: white;")




    def light_mode(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#F0F0F0"))
        self.setPalette(p)
        self.input_box.setStyleSheet(self.input_box_style+"background-color: #FFFFFF; color: black;")

        self.settingsButton.setStyleSheet(self.settingsButton_style+"background-color: #FFFFFF; color: black; ")
        self.llmsettingsButton.setStyleSheet(self.llmsettingsButton_style+"background-color: #FFFFFF; color: black; ")





    def collapse_window(self):
        the_input_box.hide()

        self.settingsButton.hide()
        self.llmsettingsButton.hide()

        self.window().setFixedSize(self.width(), 140)        



    def initUI(self):
        self.setWindowTitle("GPT")
        self.setGeometry(100, 100, 200, 200)
        self.setFixedSize(self.width()+10, self.height() + 80)

        self.first_height = self.height()
        self.first_width = self.width()



        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Custom title bar
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(30)  # Set a fixed height for the title bar
        self.title_bar.setStyleSheet("background-color: #2E2E2E; color: #fff; border-radius: 15px; border-style: solid; border-width: 1px; border-color: #303030;")

        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(5, 5, 0, 5)
        self.title_bar_layout.setSpacing(0)

        self.btn_minimize = QPushButton("_", self.title_bar)
        self.btn_minimize.setFixedSize(20, 20)
        self.btn_minimize.clicked.connect(self.showMinimized)

        def stop_app():
            self.stop_talking = True
            self.wake_word_active = False
            if MainWindow.api_enabled:
                from .api import stop_api
                stop_api()
            self.close()


        self.btn_close = QPushButton("X", self.title_bar)
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.clicked.connect(stop_app)

        self.title_label = QLabel("  "+name(), self.title_bar)
        self.title_label.setStyleSheet("border: 0px solid blue;") 

        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch()
        self.title_bar_layout.addWidget(self.btn_minimize)



        self.title_bar_layout.addWidget(self.btn_close)


        # Create a spacer item with expanding policy
        spacer = QSpacerItem(5, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title_bar_layout.addSpacerItem(spacer)  # Add spacer to the layout



        layout.addWidget(self.title_bar)




        self.drawing_widget = DrawingWidget(self)
        layout.addWidget(self.drawing_widget)






        self.layout = layout

        self.setLayout(layout)



        # Add keyboard shortcuts
        self.shortcut_screenshot = QShortcut(QKeySequence("Ctrl+1"), self)
        self.shortcut_screenshot.activated.connect(
            lambda: self.button_handler.just_screenshot()
        )
        self.shortcut_screenshot = QShortcut(QKeySequence("Ctrl+2"), self)
        self.shortcut_screenshot.activated.connect(
            lambda: self.button_handler.toggle_recording(take_system_audio=True)
        )

        self.shortcut_no_screenshot = QShortcut(QKeySequence("Ctrl+e"), self)
        self.shortcut_no_screenshot.activated.connect(
            lambda: self.button_handler.toggle_recording(take_system_audio=True)
        )

        self.shortcut_no_screenshot = QShortcut(QKeySequence("Ctrl+3"), self)
        self.shortcut_no_screenshot.activated.connect(
            lambda: self.button_handler.toggle_recording(no_screenshot=True)
        )

        # I want to create an input box to bottom left and a send button to bottom right

        input_box = CustomTextEdit(self)
        self.input_box = input_box


        input_box.setFixedHeight(80)


        if load_api_key() == "CHANGE_ME":
            input_box.setPlaceholderText("Save your API Key, go to settings")
        else:

            if platform.system() == "Darwin":
                if llm_settings[load_model_settings()]["vision"] is False:
                    input_box.setPlaceholderText("Type here \nsand ↵ ")
                else:
                    input_box.setPlaceholderText("Type here \nand ↵ \nor ⌘ + ↵ (+screenshot)")
            else:
                if llm_settings[load_model_settings()]["vision"] is False:
                    input_box.setPlaceholderText("Type here \nand ↵ ")
                else:
                    input_box.setPlaceholderText("Type here \nand ↵ \nor Ctrl + ↵ (+screenshot)")
            # Add an information and use enter icon to the input box for mac            
        input_box.setGeometry(30, self.height() - 60, 200, 80)
        global the_input_box
        the_input_box = input_box

        def input_box_send():
            if input_box.toPlainText() != "":
                click_sound()
                self.button_handler.input_text(input_box.toPlainText())

        def input_box_send_screenshot():
            if input_box.toPlainText() != "":
                click_sound()
                self.button_handler.input_text_screenshot(input_box.toPlainText())

        self.layout.addWidget(input_box)




        self.shortcut_enter = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_enter.activated.connect(input_box_send_screenshot)

        global return_key_event
        return_key_event = input_box_send



        button_layout_ = QHBoxLayout()

        self.settingsButton = QPushButton("Chat Settings", self)
        self.settingsButton.clicked.connect(settings_popup)

        self.llmsettingsButton = QPushButton("LLM Settings", self)
        self.llmsettingsButton.clicked.connect(llmsettings_popup)

        button_layout_.addWidget(self.settingsButton)
        button_layout_.addWidget(self.llmsettingsButton)
        self.layout.addLayout(button_layout_)



        self.worker = Worker()
        self.worker.text_to_set.connect(self.set_text)
        self.worker.start()

        self.worker_2 = Worker_2()
        self.worker_2.text_to_set.connect(self.start_border_animation)
        self.worker_2.text_to_set_title_bar.connect(self.set_title_bar_text)
        self.worker_2.start()

        self.worker_3 = Worker_3()
        self.worker_3.text_to_set.connect(self.general_styling)
        self.worker_3.start()


        self.worker_collapse = Worker_collapse()
        self.worker_collapse.text_to_set.connect(self.collapse_gca)
        self.worker_collapse.start()


        self.worker_uncollapse = Worker_uncollapse()
        self.worker_uncollapse.text_to_set.connect(self.uncollapse_gca)
        self.worker_uncollapse.start()


        # print height and width
        print(self.height(), self.width())

        self.show()





    def set_text(self, text):
        global the_input_box


        vertical_scrollbar = the_input_box.verticalScrollBar()
        scroll_value = vertical_scrollbar.value()



        the_input_box.setPlainText(text)

        vertical_scrollbar.setValue(scroll_value)

    def set_title_bar_text(self, text):
        self.title_label.setText(text)

    def update_from_thread(self, text, system=True):
        self.worker.make_animation = True
        if system:
            text = "System: " + text
        print("Updating from thread", text)
        self.worker.the_input_text = text

    def read_part_task_generate_only(self):
        if not is_just_text_model_active() and not the_main_window.api_enabled:


            threads = {}

            the_okey_parts = split_with_multiple_delimiters(self.worker.the_input_text,".?!:")




            for each in the_okey_parts:
                if the_main_window.stop_talking:
                    break

                
                the_thread = threading.Thread(target=text_to_speech, args=(each,))

                threads[each] = the_thread
                the_thread.start()


            for each in threads.values():
                each.join()


        self.reading_thread_2 = False

    def read_part_task(self):
        if not is_just_text_model_active() and not the_main_window.api_enabled:
            threads = {}

            the_okey_parts = split_with_multiple_delimiters(self.worker.the_input_text,".?!:")


            will_read_parts = []

            for each in the_okey_parts:
                if the_main_window.stop_talking:
                    break
                if each not in readed_sentences:
                    will_read_parts.append(each)
                    readed_sentences.append(each)

                    the_thread = threading.Thread(target=text_to_speech, args=(each,))

                    threads[each] = the_thread
                    the_thread.start()



            for each in will_read_parts:
                    if the_main_window.stop_talking:
                        break
                    threads[each].join()

                    tts_if_you_can(each, not_threaded=True, bypass_other_settings=True)


        self.reading_thread = False


    def set_text_to_input_box(self, text):
        global readed_sentences
        self.worker.make_animation = False
        if self.worker.the_input_text.startswith("System:") or self.complated_answer:
            self.worker.the_input_text = ""
            self.complated_answer = False
            readed_sentences = []
        if text not in (">", "<>", ">\n", "<", "<\n"):

            self.worker.the_input_text += text

            if self.reading_thread is not True and len(self.worker.the_input_text) > 40:
                self.reading_thread = True
                threading.Thread(target=self.read_part_task).start()

            if self.reading_thread_2 is not True and len(self.worker.the_input_text) > 250:
                self.reading_thread_2 = True
                threading.Thread(target=self.read_part_task_generate_only).start()

        else:
            print("Problem on text chars")




    def set_text_from_api(self, text):
        self.worker.make_animation = True
        self.worker.the_input_text = text










    def active_border_animation(self, title_bar_text = None):
        if self.worker_2.title_bar_text is not None:
            if self.worker_2.title_bar_text != title_bar_text:
                return

        self.worker_2.the_input_text = True
        if title_bar_text is None:
            title_bar_text = "  "+name()
        else:
            title_bar_text = f"  {title_bar_text}"
            if len(title_bar_text) > 33:
                title_bar_text = title_bar_text[:30] + "..."
        self.worker_2.title_bar_text = title_bar_text

        self.btn_minimize.hide()
        self.btn_close.hide()
    def deactive_border_animation(self, title_bar_text=None):
        
        if title_bar_text is None:
            title_bar_text = "  "+name()
        else:
            title_bar_text = f"  {title_bar_text}"
            if len(title_bar_text) > 33:
                title_bar_text = title_bar_text[:30] + "..."

        if self.worker_2.title_bar_text is not None:
            if self.worker_2.title_bar_text != title_bar_text:
                return

        self.worker_2.the_input_text = False
        self.worker_2.title_bar_text = None
        time.sleep(1)
        self.btn_minimize.show()
        self.btn_close.show()


    def mouseMoveEvent(self, event: QMouseEvent):
        delta = QPoint(event.globalPos() - self.old_position)
        if event.buttons() == Qt.LeftButton and self.title_bar.underMouse():
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()


    def mousePressEvent(self, event: QMouseEvent):
        self.old_position = event.globalPos()


    def remove_screenshot_button(self):
        self.update()


    def add_screenshot_button(self):
        self.update()


    def update_state(self, new_state):

        assistant_stopped = False
        if self.state == "aitalking" and new_state == "idle":
            assistant_stopped = True

        if self.manuel_stop:
            assistant_stopped = False
            self.manuel_stop = False



        self.state = new_state
        print(f"State updated: {new_state}")
        if "talking" in new_state:
            self.tray.setIcon(self.tray_active_icon)
            self.pulse_frame = 0
            if self.pulse_timer:
                self.pulse_timer.stop()
                self.pulse_timer = None
            self.pulse_timer = QTimer(self)
            self.pulse_timer.timeout.connect(self.pulse_circle)
            self.pulse_timer.start(5)
        elif new_state == "thinking":

            the_main_window.update_from_thread("Thinking...")
            self.pulse_frame = 0
            if self.pulse_timer:
                self.pulse_timer.stop()
                self.pulse_timer = None
            self.pulse_timer = QTimer(self)
            self.pulse_timer.timeout.connect(self.pulse_circle)
            self.pulse_timer.start(20)
        elif self.pulse_timer:
            self.tray.setIcon(self.tray_icon)
            self.pulse_timer.stop()
            self.pulse_timer = None
        self.update()  # Trigger a repaint

        if assistant_stopped:
            
                global the_input_box
                if the_input_box.toPlainText().endswith("?") and is_continuously_conversations_setting_active():
                    
                    self.button_handler.toggle_recording(no_screenshot=True, new_record=True)

        if new_state == "idle":
            click_sound()

    def pulse_circle(self):
        self.pulse_frame = (self.pulse_frame + 1) % 100
        self.update()




    def collapse_gca(self):
        self.collapse = True
        self.collapse_window()
        activate_collapse_setting()

    def collapse_gca_api(self):
        self.worker_collapse.the_input_text = "True"


    def uncollapse_gca(self):
        self.collapse = False
        print()
        # hide all buttons and input box
        the_input_box.show()

        self.settingsButton.show()
        self.llmsettingsButton.show()

        self.window().setFixedSize(self.first_width, self.first_height)
        deactivate_collapse_setting()


    def uncollapse_gca_api(self):
        self.worker_uncollapse.the_input_text = "True"
        