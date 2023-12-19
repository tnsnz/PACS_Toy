from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit


def create_horizontal_label_line_edit(obj, variable_key: str):
    frame_key = variable_key + '_frame'
    line_edit_key = variable_key + '_line_edit'

    frame = QFrame()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)
    frame.setLayout(layout)

    label = QLabel(variable_key)
    line_edit = QLineEdit()

    layout.addWidget(label)
    layout.addWidget(line_edit)

    obj.__setattr__(frame_key, frame)
    obj.__setattr__(line_edit_key, line_edit)
