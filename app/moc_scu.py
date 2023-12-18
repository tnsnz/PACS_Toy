import os
import sys
import traceback

from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtWidgets import QFileDialog, QApplication
from pydicom import dcmread
from pynetdicom import AE
from pynetdicom.apps.common import setup_logging
from pynetdicom.apps.storescu.storescu import _setup_argparser
from pynetdicom.sop_class import CTImageStorage

from filemanager import FileManager


class FindSCU:
    def __init__(self):
        pass


class StoreSCU:
    def __init__(self, is_dir):
        # debug_logger()
        self.is_dir = is_dir
        self.ae = AE()
        self.ae.add_requested_context(CTImageStorage)

    def request(self, args, fpath):
        qet = QElapsedTimer()
        qet.start()

        app_logger = setup_logging(args, "storescu")
        assoc = self.ae.associate("127.0.0.1", 11112)

        dicom_files = FileManager().get_dicom_files(fpath)

        if assoc.is_established:
            for file in dicom_files:
                ds = dcmread(file)
                status = assoc.send_c_store(ds)

                if 0xA700 == status.Status or 0xA701 == status.Status:
                    app_logger.error("Could not write file to specified directory:")
                    app_logger.error(f"{os.path.dirname(file)}")
                    app_logger.exception(traceback.format_exc())

        assoc.release()
        print(qet.elapsed() / 1000.0, 'sec')


class GetSCU:
    def __init__(self):
        pass


def main(args):
    if args is not None:
        sys.argv = args

    args = _setup_argparser()

    a = QApplication(sys.argv)
    is_dir = True

    if is_dir:
        selected_files = [QFileDialog.getExistingDirectory(
            None,
            "Select Directory",
            ""
        )]
    else:
        selected_files = QFileDialog.getOpenFileNames(
            None,
            "Select Files",
            ""
        )[0]

    scu = StoreSCU(is_dir)
    scu.request(args, selected_files)
    a.exec()


if __name__ == '__main__':
    main(['moc_scu.py', 'localhost', '11112', r'C:\Users\tndns\Desktop\workspace\origin\PACS_Toy\app\store_dir'])
