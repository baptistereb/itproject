#pip install PyQt6
#pip install fitz
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QCheckBox, QLabel, QDoubleSpinBox, QLineEdit, QTextBrowser, QPushButton, QHBoxLayout, QVBoxLayout, QWidget,QPlainTextEdit, QProgressBar, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap, QTransform
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.exercise=0
        self.mistakes = ["-1 calculus", "-2 explanations", "-42 because why not", "-3 ?", "-0.5 test"]
        self.studentAnswer = [[["A good answer", "Another", "try something"], ["b1", "b2", "b3"],["c1", "c2", "c3"]], [["q1", "q2", "q3"], ["b1", "b2", "b3"],["c1", "c2", "c3"]], [["Student 2 - q1", "q2", "q3"], ["b1", "b2", "b3"],["c1", "c2", "c3"]]]
        self.totalStudents=len(self.studentAnswer)

        self.showFirstWindow()

    def changeExercise(self,num):
        self.exercise=num
        self.showWindow(self.questions)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select a File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                print("Selected file:", file_path)
                self.changeStudent(0)

    def changeStudent(self,num):
        if num >= 0 and num <= self.totalStudents:
            self.studentNbr=num

            if self.studentNbr != self.totalStudents:
                self.questions = self.studentAnswer[self.studentNbr]
                self.showWindow(self.questions)
            else:
                self.showLastWindow()

    def UpdateProgressBar(self):
        ratio = int(100*(self.studentNbr/self.totalStudents))
        self.progressBarWidget.setValue(ratio)

    def addMistake(self):
        self.mistakes.append("-"+ str(self.errorNum.value()) + " " + self.errorText.text())
        self.errorNum.setValue(1.0)
        self.errorText.clear()
        self.showWindow(self.questions)

    def showFirstWindow(self):
        self.setWindowTitle("File Upload Example")
        self.setGeometry(100, 100, 400, 200)

        upload_button = QPushButton("Upload File", self)
        upload_button.setGeometry(150, 80, 100, 30)
        upload_button.clicked.connect(self.upload_file)
        #self.showWindow(self.questions)
        self.show()

    def showLastWindow(self):
        self.setWindowTitle("IT Project - Finish")
        self.UpdateProgressBar()

        content = QHBoxLayout()

        dlResultButton = QPushButton("Download Result")
        dlResultButton.setCheckable(True)
        #dlResultButton.pressed.connect()
        content.addWidget(dlResultButton)

        footerBar = QVBoxLayout()
        nextPreviousBar = QHBoxLayout()
        progressBar = QHBoxLayout()

        previousStudent = QPushButton("Previous Student")
        previousStudent.setCheckable(True)
        previousStudent.pressed.connect(lambda: self.changeStudent(self.totalStudents-1))
        nextPreviousBar.addWidget(previousStudent)

        self.UpdateProgressBar()
        progressBar.addWidget(self.progressBarWidget)
        
        footerBar.addLayout(nextPreviousBar)
        footerBar.addLayout(progressBar)

        AllLayoutLastWindow = QVBoxLayout()
        AllLayoutLastWindow.addLayout(content)

        AllLayoutLastWindow.addLayout(footerBar)


        widget = QScrollArea()
        widget.setLayout(AllLayoutLastWindow)
        self.setCentralWidget(widget)

        self.show()
    
    def showWindow(self, data):
        self.setWindowTitle("IT Project - Exercise "+str(self.exercise+1))
        self.setFixedSize(QSize(1000, 500))
        #self.showFullScreen()

        self.progressBarWidget = QProgressBar()
        self.errorText = QLineEdit()
        self.errorNum = QDoubleSpinBox()

        #MENU
        menu = QHBoxLayout()
        for i in range(len(data)):
            button = QPushButton("Exercise "+str(i+1))
            button.setCheckable(True)
            button.pressed.connect(lambda i=i: self.changeExercise(i))
            menu.addWidget(button)

        leftBar = QVBoxLayout()
        leftBar.addLayout(menu)

        #STUDENT ANSWER
        for i in data[self.exercise]:
            question = QTextBrowser()
            question.setPlainText(i)
            leftBar.addWidget(question)

        rightBar = QVBoxLayout()

        #ANSWER
        correction = QLabel(self)
        
        correctionPixmap = QPixmap("./test.jpg")

        ratio = (self.width() // 2) / correctionPixmap.width()
        newHeight = int(correctionPixmap.height() * ratio)
        correctionPixmap = correctionPixmap.scaled(self.width() // 3, newHeight)
        correction.setPixmap(correctionPixmap)
        correction.setScaledContents(True)

        rightBar.addWidget(correction)

        midBar = QVBoxLayout()
        
        #MISTAKES ADD & SELECT
        errorAddBar = QHBoxLayout()
        errorAdd = QPushButton("Add Mistake")
        errorAdd.clicked.connect(self.addMistake)
        errorAddBar.addWidget(self.errorText)
        errorAddBar.addWidget(self.errorNum)
        errorAddBar.addWidget(errorAdd)


        midBar.addLayout(errorAddBar)

        for i in self.mistakes:
            ms = QCheckBox()
            ms.setText(i)
            midBar.addWidget(ms)

        content = QHBoxLayout()
        content.addLayout(leftBar)
        content.addLayout(midBar)
        content.addLayout(rightBar)

        footerBar = QVBoxLayout()
        nextPreviousBar = QHBoxLayout()
        progressBar = QHBoxLayout()

        previousStudent = QPushButton("Previous Student")
        previousStudent.setCheckable(True)
        previousStudent.pressed.connect(lambda i=self.studentNbr-1: self.changeStudent(i))
        nextStudent = QPushButton("Next Student")
        nextStudent.setCheckable(True)
        nextStudent.pressed.connect(lambda i=self.studentNbr+1: self.changeStudent(i))
        nextPreviousBar.addWidget(previousStudent)
        nextPreviousBar.addWidget(nextStudent)


        self.UpdateProgressBar()
        progressBar.addWidget(self.progressBarWidget)
        
        footerBar.addLayout(nextPreviousBar)
        footerBar.addLayout(progressBar)


        AllLayout = QVBoxLayout()
        AllLayout.addLayout(content)
        AllLayout.addLayout(footerBar)

        widget = QScrollArea()
        widget.setLayout(AllLayout)
        self.setCentralWidget(widget)

        self.show()


app = QApplication(sys.argv)

window = MainWindow()
#window.test("vvvv")

app.exec()