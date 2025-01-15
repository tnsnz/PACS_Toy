import sys

from PyQt5.QtWidgets import QApplication


def exec_qapplication(widget_cls: type):
    a = QApplication(sys.argv)

    w = widget_cls()

    style: str = ''

    try:
        style = open('resources/dark_teal.qss', 'r').read()
    except Exception as e:
        print(e.__traceback__)

    w.setStyleSheet(style)
    w.show()

    yield a.exec()
