import os
import sys

from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtWidgets import QFileDialog, QApplication
from pydicom import dcmread
from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import CTImageStorage


class FindSCU:
    def __init__(self):
        pass


class StoreSCU:
    def __init__(self, is_dir):
        # debug_logger()

        self.is_dir = is_dir

        self.ae = AE()
        self.ae.add_requested_context(CTImageStorage)

    def request(self, selected_files):
        qet = QElapsedTimer()
        qet.start()
        assoc = self.ae.associate("127.0.0.1", 11112)

        if assoc.is_established:
            if (self.is_dir):
                for file_name in os.listdir(selected_files):
                    file = os.path.join(selected_files, file_name)
                    ds = dcmread(file)
                    assoc.send_c_store(ds)
            else:
                for file in selected_files:
                    ds = dcmread(file)
                    assoc.send_c_store(ds)

        assoc.release()
        print(qet.elapsed() / 1000.0, 'sec')


class GetSCU:
    def __init__(self):
        pass


def main():
    a = QApplication(sys.argv)
    is_dir = True

    file_dialog = QFileDialog()
    if is_dir:
        selected_files = QFileDialog.getExistingDirectory(
            None,
            "Select Directory",
            ""
        )
    else:
        selected_files = QFileDialog.getOpenFileNames(
            None,
            "Select Files",
            ""
        )

    print(selected_files)
    scu = StoreSCU(is_dir)
    scu.request(selected_files)
    a.exec()


if __name__ == '__main__':
    main()
