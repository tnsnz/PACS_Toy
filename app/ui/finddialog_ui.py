from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QTreeWidget, QPushButton, \
    QLabel, QComboBox

from custom_widgets import create_horizontal_label_line_edit


class FindDialog_ui:
    def __init__(self, FindDialog):
        FindDialog.setFixedSize(1920, 1080)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        FindDialog.setLayout(layout)

        self.qry_info_frame = QFrame()
        self.dir_frame = QFrame()
        self.reg_frame = QFrame()
        self.store_get_frame = QFrame()
        self.dir_tree_widget = QTreeWidget()

        self.qry_retrieve_combobox = QComboBox()

        self.store_btn = QPushButton('Store')
        self.store_btn.clicked.connect(FindDialog.store_dicom)

        self.get_btn = QPushButton('Get')
        self.get_btn.clicked.connect(FindDialog.get_dicom)

        self.find_btn = QPushButton('Find')
        self.find_btn.clicked.connect(FindDialog.request_find)

        dir_layout = QVBoxLayout()
        self.dir_frame.setLayout(dir_layout)

        store_get_layout = QHBoxLayout()
        self.store_get_frame.setLayout(store_get_layout)

        store_get_layout.addWidget(self.store_btn)
        store_get_layout.addWidget(self.get_btn)

        dir_layout.addWidget(self.dir_tree_widget)
        dir_layout.addWidget(self.store_get_frame)

        reg_layout = QVBoxLayout()
        reg_layout.setContentsMargins(0, 0, 0, 0)
        reg_layout.setSpacing(10)
        self.reg_frame.setLayout(reg_layout)

        qry_info_layout = QHBoxLayout()
        qry_info_layout.setContentsMargins(0, 0, 0, 0)
        qry_info_layout.setSpacing(10)
        self.qry_info_frame.setLayout(qry_info_layout)

        qry_retrieve_label = QLabel('Query Retrieve')
        self.qry_retrieve_combobox.addItem('PATIENT')
        self.qry_retrieve_combobox.addItem('STUDY')
        self.qry_retrieve_combobox.addItem('SERIES')
        self.qry_retrieve_combobox.setCurrentIndex(0)

        qry_info_layout.addWidget(qry_retrieve_label)
        qry_info_layout.addWidget(self.qry_retrieve_combobox)

        create_horizontal_label_line_edit(self, 'patient_id')
        create_horizontal_label_line_edit(self, 'patient_name')
        create_horizontal_label_line_edit(self, 'study_id')
        create_horizontal_label_line_edit(self, 'series_number')

        reg_layout.addWidget(self.qry_info_frame)
        reg_layout.addWidget(self.patient_id_frame)
        reg_layout.addWidget(self.patient_name_frame)
        reg_layout.addWidget(self.study_id_frame)
        reg_layout.addWidget(self.series_number_frame)

        layout.addWidget(self.dir_frame)
        layout.addWidget(self.reg_frame)
        layout.addWidget(self.find_btn)
