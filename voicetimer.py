import sys
import os
import numpy as np
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QInputDialog, QSlider, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

# Initialize pygame mixer
pygame.mixer.init()

class TimerApp(QWidget):
    def __init__(self, x=100, y=100):
        super().__init__()

        self.counter = 0
        self.countdown = 40
        self.isPaused = False

        self.initUI(x, y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.beep)
        self.timer.start(1000)

    def initUI(self, x, y):
        self.setWindowTitle('Sleek Timer App')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setGeometry(x, y, 400, 250)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setPalette(palette)

        sleekFont = QFont('Roboto', 24, QFont.Bold)

        self.counterLabel = QLabel(f'Counter: {self.counter}', self)
        self.counterLabel.setFont(sleekFont)

        self.countdownLabel = QLabel(f'Countdown: {self.countdown}', self)
        self.countdownLabel.setFont(sleekFont)

        self.restartButton = QPushButton('Restart', self)
        self.restartButton.setFont(QFont('Roboto', 16))
        self.restartButton.setStyleSheet('background-color: black; color: white')
        self.restartButton.clicked.connect(self.restartApp)

        self.pauseButton = QPushButton('Pause/Start Timer', self)
        self.pauseButton.setFont(QFont('Roboto', 16))
        self.pauseButton.setStyleSheet('background-color: black; color: white')
        self.pauseButton.clicked.connect(self.pauseTimer)

        self.setCounterButton = QPushButton('Set Counter', self)
        self.setCounterButton.setFont(QFont('Roboto', 16))
        self.setCounterButton.setStyleSheet('background-color: black; color: white')
        self.setCounterButton.clicked.connect(self.setCounter)

        self.setTimerButton = QPushButton('Set Timer', self)
        self.setTimerButton.setFont(QFont('Roboto', 16))
        self.setTimerButton.setStyleSheet('background-color: black; color: white')
        self.setTimerButton.clicked.connect(self.setTimer)

        # Volume Slider
        self.volumeSlider, self.volumeLabel = self.createVolumeSlider()
        self.volumeSlider.valueChanged.connect(self.adjustVolume)

        # Layout for the volume controls
        volumeLayout = QHBoxLayout()
        volumeLayout.addWidget(self.volumeLabel)
        volumeLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.counterLabel)
        layout.addWidget(self.countdownLabel)
        layout.addLayout(volumeLayout)
        layout.addWidget(self.restartButton)
        layout.addWidget(self.pauseButton)
        layout.addWidget(self.setCounterButton)
        layout.addWidget(self.setTimerButton)

        self.setLayout(layout)
        self.show()

    def createVolumeSlider(self):
        volumeLabel = QLabel('Volume:', self)
        volumeLabel.setFont(QFont('Roboto', 16))
        volumeLabel.setStyleSheet('color: white')

        volumeSlider = QSlider(Qt.Horizontal, self)
        volumeSlider.setFocusPolicy(Qt.StrongFocus)
        volumeSlider.setTickPosition(QSlider.TicksBothSides)
        volumeSlider.setTickInterval(10)
        volumeSlider.setSingleStep(1)
        volumeSlider.setMinimum(0)
        volumeSlider.setMaximum(100)
        volumeSlider.setValue(100)  # Default volume: 100%
        volumeSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                height: 8px;
                background: white;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ee9a00, stop:1 #ffc041);
                border: 1px solid #777;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)
        return volumeSlider, volumeLabel

    def beep(self):
        if not self.isPaused:
            self.countdown -= 1
            self.countdownLabel.setText(f'Countdown: {self.countdown}')

            if self.countdown == 0:
                audio_files = [
                    os.path.join("audio", "next_job1.mp3"),
                    os.path.join("audio", "next_job2.mp3"),
                    os.path.join("audio", "next_job3.mp3"),
                    os.path.join("audio", "next_job4.mp3"),
                    os.path.join("audio", "next_job5.mp3"),
                ]
                chosen_file = np.random.choice(audio_files)
                pygame.mixer.music.load(chosen_file)
                pygame.mixer.music.set_volume(self.volumeSlider.value() / 100.0)
                pygame.mixer.music.play()
            
                self.counter += 1
                self.counterLabel.setText(f'Counter: {self.counter}')
                self.countdown = 40

    def adjustVolume(self):
        volume_level = self.volumeSlider.value() / 100.0
        pygame.mixer.music.set_volume(volume_level)

    def restartApp(self):
        self.buttonEffect(self.restartButton)
        self.timer.stop()
        x, y = self.x(), self.y() + 30
        self.close()
        self.__init__(x, y)
        self.timer.start(1000)

    def pauseTimer(self):
        self.buttonEffect(self.pauseButton)
        self.isPaused = not self.isPaused

    def setCounter(self):
        self.buttonEffect(self.setCounterButton)
        num, ok = QInputDialog.getInt(self, 'Set Counter', 'Enter the new counter value:')
        if ok:
            self.counter = num
            self.counterLabel.setText(f'Counter: {self.counter}')

    def setTimer(self):
        self.buttonEffect(self.setTimerButton)
        num, ok = QInputDialog.getInt(self, 'Set Timer', 'Enter the new timer value:')
        if ok:
            self.countdown = num
            self.countdownLabel.setText(f'Countdown: {self.countdown}')

    def buttonEffect(self, button):
        button.setStyleSheet('background-color: red; color: white')
        QTimer.singleShot(200, lambda: button.setStyleSheet('background-color: black; color: white'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    sys.exit(app.exec_())