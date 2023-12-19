from typing import List

from PyQt5.QtWidgets import QDialog, QWidget, QFileDialog, QTreeWidgetItem
from pydicom import Dataset

from dataset_handler import DatasetDecoder
from god import FindQuery
from moc_scu import FindSCU
from ui.finddialog_ui import FindDialog_ui as UI


class FindDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super(FindDialog, self).__init__(parent)
        self.ui = UI(self)
        self.find_scu = FindSCU()

    def request_find(self):
        p_id = self.ui.patient_id_line_edit.text()
        p_name = self.ui.patient_name_line_edit.text()
        s_id = self.ui.study_id_line_edit.text()
        s_num = self.ui.series_number_line_edit.text()
        level = self.ui.qry_retrieve_combobox.currentText()
        fq = FindQuery(p_id, p_name, s_id, s_num, qry=level)

        ret = self.find_scu.process(fq)
        self.refresh_tree(ret)

    def store_dicom(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.exec()
        selected_files = file_dialog.selectedFiles()
        print(selected_files)

    def get_dicom(self):
        pass

    def refresh_tree(self, ds_list: List[Dataset]):
        if None is ds_list or 0 == len(ds_list):
            return

        self.ui.dir_tree_widget.clear()
        root = self.ui.dir_tree_widget.invisibleRootItem()

        for ds in ds_list:
            pickled = DatasetDecoder(ds)
            p_id = pickled.p_id
            p_name = pickled.p_name

            assert isinstance(p_id, str) or '' == p_id
            assert isinstance(p_name, str) or '' == p_name

            patient_item = QTreeWidgetItem([p_name + '_' + p_id])
            root.addChild(patient_item)

            if pickled.s_id_valid:
                study_item = QTreeWidgetItem([pickled.s_id])
                patient_item.addChild(study_item)

            if pickled.s_num_valid:
                s_series = pickled.s_num
                series_item = QTreeWidgetItem([s_series])
                study_item.addChild(series_item)
