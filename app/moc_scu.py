import os
import sys
import traceback

from PyQt5.QtCore import QElapsedTimer
from PyQt5.QtWidgets import QApplication
from pydicom import dcmread
from pynetdicom import AE
from pynetdicom.apps.common import setup_logging
from pynetdicom.apps.storescu.storescu import _setup_argparser
from pynetdicom.sop_class import (CTImageStorage,
                                  PatientRootQueryRetrieveInformationModelFind)

from executor import exec_qapplication
from filemanager import FileManager
from god import FindQuery


class FindSCU:
    def __init__(self):
        self.ae = AE()
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

    def process(self, qry: FindQuery):
        assoc = self.ae.associate("127.0.0.1", 11112)

        ds = qry.toDataset()
        if assoc.is_established:
            ds_set = []
            responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if 0xFF00 == status.Status:
                    ds_set.append(identifier)
                elif 0 == status.Status:
                    print('succeed get response from scp')
                else:
                    print('Connection timed out, was aborted or received invalid response')

            assoc.release()
            return ds_set
        else:
            print('Association rejected, aborted or never connected')


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
    # have to resolve circular dependency issue
    from moc_find_ui import FindDialog

    if args is not None:
        sys.argv = args

    args = _setup_argparser()

    executor = exec_qapplication(FindDialog)
    executor.__next__()


if __name__ == '__main__':
    main(['moc_scu.py', 'localhost', '11112', r'C:\Users\tndns\Desktop\workspace\origin\PACS_Toy\app\store_dir'])
