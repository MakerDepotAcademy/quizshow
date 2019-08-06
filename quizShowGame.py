from PyQt5 import QtCore, QtGui, QtWidgets
import sys  # We need sys so that we can pass argv to QApplication

import quizShowUi
from triviaDb import triviaDb

class quizShowGame(QtWidgets.QMainWindow, quizShowUi.Ui_Form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


def main():
    tq = triviaDb()
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    database = "/Users/fcorn/tmp/quizShow.db"
    conn = tq.create_connection(database)
    form = QtWidgets.QWidget()
    ui = quizShowUi.Ui_Form()
    ui.setupUi(form)

    # Get question loop

    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
