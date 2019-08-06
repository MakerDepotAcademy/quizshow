# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quizShowUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(666, 476)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.screenLeftGridLayout = QtWidgets.QGridLayout()
        self.screenLeftGridLayout.setObjectName("screenLeftGridLayout")
        self.horizontalLayout.addLayout(self.screenLeftGridLayout)
        self.formGridLayout = QtWidgets.QGridLayout()
        self.formGridLayout.setObjectName("formGridLayout")
        self.senterGridLayout = QtWidgets.QGridLayout()
        self.senterGridLayout.setObjectName("senterGridLayout")
        self.questionLabel = QtWidgets.QLabel(Form)
        self.questionLabel.setStyleSheet("background-color: rgb(111, 255, 218);\n"
"font: 32pt \".SF NS Text\";\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-radius: 50px;")
        self.questionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.questionLabel.setWordWrap(True)
        self.questionLabel.setObjectName("questionLabel")
        self.senterGridLayout.addWidget(self.questionLabel, 0, 0, 1, 1)
        self.bottomLine = QtWidgets.QFrame(Form)
        self.bottomLine.setSizeIncrement(QtCore.QSize(0, 1))
        self.bottomLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.bottomLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.bottomLine.setObjectName("bottomLine")
        self.senterGridLayout.addWidget(self.bottomLine, 2, 0, 1, 1)
        self.bottomGridLayout = QtWidgets.QGridLayout()
        self.bottomGridLayout.setObjectName("bottomGridLayout")
        self.scoreLabel = QtWidgets.QLabel(Form)
        self.scoreLabel.setObjectName("scoreLabel")
        self.bottomGridLayout.addWidget(self.scoreLabel, 0, 0, 1, 1)
        self.scoreValueLabel = QtWidgets.QLabel(Form)
        self.scoreValueLabel.setObjectName("scoreValueLabel")
        self.bottomGridLayout.addWidget(self.scoreValueLabel, 0, 1, 1, 1)
        self.timeValueLabel = QtWidgets.QLabel(Form)
        self.timeValueLabel.setObjectName("timeValueLabel")
        self.bottomGridLayout.addWidget(self.timeValueLabel, 0, 4, 1, 1)
        self.timeLabel = QtWidgets.QLabel(Form)
        self.timeLabel.setObjectName("timeLabel")
        self.bottomGridLayout.addWidget(self.timeLabel, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottomGridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.senterGridLayout.addLayout(self.bottomGridLayout, 3, 0, 1, 1)
        self.answersGridLayout = QtWidgets.QGridLayout()
        self.answersGridLayout.setObjectName("answersGridLayout")
        self.yellowAnswerLabel = QtWidgets.QLabel(Form)
        self.yellowAnswerLabel.setStyleSheet("background-color: rgb(255, 255, 10);\n"
"font: 32pt \".SF NS Text\";\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-radius: 20px;")
        self.yellowAnswerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yellowAnswerLabel.setObjectName("yellowAnswerLabel")
        self.answersGridLayout.addWidget(self.yellowAnswerLabel, 0, 0, 1, 1)
        self.redAnswerLabel = QtWidgets.QLabel(Form)
        self.redAnswerLabel.setStyleSheet("background-color: rgb(252, 1, 7);\n"
"font: 32pt \".SF NS Text\";\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-radius: 20px;")
        self.redAnswerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.redAnswerLabel.setObjectName("redAnswerLabel")
        self.answersGridLayout.addWidget(self.redAnswerLabel, 0, 1, 1, 1)
        self.greenAnswerLabel = QtWidgets.QLabel(Form)
        self.greenAnswerLabel.setStyleSheet("background-color: rgb(33, 255, 6);\n"
"font: 32pt \".SF NS Text\";\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-radius: 20px;")
        self.greenAnswerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.greenAnswerLabel.setObjectName("greenAnswerLabel")
        self.answersGridLayout.addWidget(self.greenAnswerLabel, 1, 0, 1, 1)
        self.blueAnswerLabel = QtWidgets.QLabel(Form)
        self.blueAnswerLabel.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"font: 32pt \".SF NS Text\";\n"
"border-width: 1px;\n"
"border-style: solid;\n"
"border-radius: 20px;")
        self.blueAnswerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blueAnswerLabel.setObjectName("blueAnswerLabel")
        self.answersGridLayout.addWidget(self.blueAnswerLabel, 1, 1, 1, 1)
        self.senterGridLayout.addLayout(self.answersGridLayout, 1, 0, 1, 1)
        self.senterGridLayout.setRowStretch(0, 2)
        self.senterGridLayout.setRowStretch(1, 2)
        self.senterGridLayout.setRowStretch(2, 2)
        self.senterGridLayout.setRowStretch(3, 1)
        self.formGridLayout.addLayout(self.senterGridLayout, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.formGridLayout)
        self.screenRightGridLayout = QtWidgets.QGridLayout()
        self.screenRightGridLayout.setObjectName("screenRightGridLayout")
        self.horizontalLayout.addLayout(self.screenRightGridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.questionLabel.setText(_translate("Form", "When a pirate yells, \'Avast, ye mateys\' he is telling his mates to do what?"))
        self.scoreLabel.setText(_translate("Form", "Score"))
        self.scoreValueLabel.setText(_translate("Form", "000"))
        self.timeValueLabel.setText(_translate("Form", "00:00"))
        self.timeLabel.setText(_translate("Form", "Timer"))
        self.yellowAnswerLabel.setText(_translate("Form", "Stop"))
        self.redAnswerLabel.setText(_translate("Form", "Drink"))
        self.greenAnswerLabel.setText(_translate("Form", "Fight"))
        self.blueAnswerLabel.setText(_translate("Form", "Run"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
