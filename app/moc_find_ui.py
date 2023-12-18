import sys

from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QFrame, QVBoxLayout, QTreeWidget, QPushButton, \
    QLabel, QComboBox, QLineEdit, QFileDialog, QTreeWidgetItem

from god import FindQuery
from moc_scu import FindSCU


class FindDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        QDialog.__init__(self, parent)

        self.find_scu = FindSCU()
        self.setup()

    def setup(self):
        self.setFixedSize(1920, 1080)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.dir_frame = QFrame()
        dir_layout = QVBoxLayout()
        self.dir_frame.setLayout(dir_layout)

        self.dir_tree_widget = QTreeWidget()
        layout.addWidget(self.dir_tree_widget)

        self.store_btn = QPushButton('Store')
        self.store_btn.clicked.connect(self.store_dicom)

        self.get_btn = QPushButton('Get')
        self.get_btn.clicked.connect(self.get_dicom)

        self.store_get_frame = QFrame()
        store_get_layout = QHBoxLayout()
        self.store_get_frame.setLayout(store_get_layout)

        store_get_layout.addWidget(self.store_btn)
        store_get_layout.addWidget(self.get_btn)

        dir_layout.addWidget(self.dir_tree_widget)
        dir_layout.addWidget(self.store_get_frame)

        layout.addWidget(self.dir_frame)

        self.reg_frame = QFrame()
        reg_layout = QVBoxLayout()
        reg_layout.setContentsMargins(0, 0, 0, 0)
        reg_layout.setSpacing(10)
        self.reg_frame.setLayout(reg_layout)

        self.qry_info_frame = QFrame()
        qry_info_layout = QHBoxLayout()
        qry_info_layout.setContentsMargins(0, 0, 0, 0)
        qry_info_layout.setSpacing(10)
        self.qry_info_frame.setLayout(qry_info_layout)

        qry_retrieve_label = QLabel('Query Retrieve')
        self.qry_retrieve_combobox = QComboBox()
        self.qry_retrieve_combobox.addItem('PATIENT')
        self.qry_retrieve_combobox.addItem('STUDY')
        self.qry_retrieve_combobox.addItem('SERIES')
        self.qry_retrieve_combobox.setCurrentIndex(0)

        qry_info_layout.addWidget(qry_retrieve_label)
        qry_info_layout.addWidget(self.qry_retrieve_combobox)

        self.patient_id_frame = QFrame()
        patient_id_layout = QHBoxLayout()
        patient_id_layout.setContentsMargins(0, 0, 0, 0)
        patient_id_layout.setSpacing(10)
        self.patient_id_frame.setLayout(patient_id_layout)

        patient_id_label = QLabel('Patient ID')
        self.patient_id_line_edit = QLineEdit()
        patient_id_layout.addWidget(patient_id_label)
        patient_id_layout.addWidget(self.patient_id_line_edit)

        self.patient_name_frame = QFrame()
        patient_name_layout = QHBoxLayout()
        patient_name_layout.setContentsMargins(0, 0, 0, 0)
        patient_name_layout.setSpacing(10)
        self.patient_name_frame.setLayout(patient_name_layout)

        patient_name_label = QLabel('Patient Name')
        self.patient_name_line_edit = QLineEdit()

        patient_name_layout.addWidget(patient_name_label)
        patient_name_layout.addWidget(self.patient_name_line_edit)

        reg_layout.addWidget(self.qry_info_frame)
        reg_layout.addWidget(self.patient_id_frame)
        reg_layout.addWidget(self.patient_name_frame)

        self.find_btn = QPushButton('Find')

        layout.addWidget(self.reg_frame)
        layout.addWidget(self.find_btn)

        self.find_btn.clicked.connect(self.request_find)

    def request_find(self):
        p_id = self.patient_id_line_edit.text()
        p_name = self.patient_name_line_edit.text()
        level = self.qry_retrieve_combobox.currentText()
        fq = FindQuery(p_id=p_id, p_name=p_name, qry=level)

        ret = self.find_scu.process(fq)
        self.foo(ret)

    def get_dicom(self):
        pass

    def store_dicom(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.exec()
        selected_files = file_dialog.selectedFiles()
        print(selected_files)

    def foo(self, l):
        print(l)
        if None == l or 0 == len(l):
            return

        self.dir_tree_widget.clear()

        root = self.dir_tree_widget.invisibleRootItem()

        for ds in l:
            p_id = ds.PatientID
            p_name = ds.PatientName.components[0]
            s_id = ds.StudyID

            s_series = ds.SeriesNumber.original_string
            patient_item = QTreeWidgetItem([p_name + '_' + p_id])
            root.addChild(patient_item)

            study_item = QTreeWidgetItem([s_id])
            patient_item.addChild(study_item)

            series_item = QTreeWidgetItem([s_series])
            study_item.addChild(series_item)
