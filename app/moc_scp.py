import os
import re
import sys

from pydicom import Dataset
from pydicom.uid import DeflatedExplicitVRLittleEndian, CTImageStorage
from pynetdicom import (
    AE,
    evt,
    debug_logger,
    AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES,
    events
)

from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

from pynetdicom.apps.common import setup_logging
from pynetdicom.apps.storescp.storescp import _setup_argparser

from dataset_decoder import DatasetDecoder
from filemanager import FileManager
from local_storage import LocalStorage

debug_logger()

local_storage = LocalStorage()

class FindSCP:
    def __init__(self):
        # Initialise the Application Entity and specify the listen port
        self.ae = AE()

        # Add the supported presentation context
        self.ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

        for cx in AllStoragePresentationContexts:
            self.ae.add_supported_context(cx.abstract_syntax, ALL_TRANSFER_SYNTAXES)

        self.handlers = [(evt.EVT_C_FIND, self.handle_find)]

        # Start listening for incoming association requests
        self.ae.start_server(("127.0.0.1", 11112), evt_handlers=self.handlers)

    def handle_find(self, event: events.Event, args, app_logger):
        ds = event.dataset

        if 'QueryRetrieveLevel' not in ds:
            # Failure
            yield 0xC000, None
            return

        level = ds.QueryRetrieveLevel

        local_storage.find_files_in_dataset(DatasetDecoder(ds), level)

class StoreSCP:
    def __init__(self, args):
        if args is not None:
            sys.argv = args

        args = _setup_argparser()
        APP_LOGGER = setup_logging(args, "storescp")

        ae = AE()
        ae.acse_timeout = 5
        ae.dimse_timeout = 5
        ae.network_timeout = 5
        ae.add_supported_context(CTImageStorage)

        for cx in AllStoragePresentationContexts:
            ae.add_supported_context(cx.abstract_syntax, ALL_TRANSFER_SYNTAXES)

        handlers = [(evt.EVT_C_STORE, self.handle_store, [args, APP_LOGGER])]

        ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)

    def sanitize_uid(self, uid):
        return re.sub(r"[^\d.]", "_", uid)

    def handle_store(self, event: events.Event, args, app_logger):
        status_ds = Dataset()
        status_ds.Status = 0x0000

        dataset_binary = event.request.DataSet.getvalue()

        ds = event.dataset
        f_manager = FileManager()
        filename = ''

        try:
            decoded_ds = DatasetDecoder(ds)
            sanitized_uid = self.sanitize_uid(ds.SOPInstanceUID)
            filename = f_manager.target_file(decoded_ds, sanitized_uid)

            if event.context.transfer_syntax == DeflatedExplicitVRLittleEndian:
                f_manager.deflated_store(filename, ds, dataset_binary)
            else:
                f_manager.store(filename, ds)
        except OSError as exc:
            app_logger.error("Could not write file to specified directory:")
            app_logger.error(f"    {os.path.dirname(filename)}")
            app_logger.exception(exc)
            # Failed - Out of Resources - OSError
            status_ds.Status = 0xA700
        except Exception as exc:
            app_logger.error("Could not write file to specified directory:")
            app_logger.error(f"    {os.path.dirname(filename)}")
            app_logger.exception(exc)
            # Failed - Out of Resources - Miscellaneous error
            status_ds.Status = 0xA701

        return status_ds


class GetSCP:
    def __init__(self):
        pass


def main(args=None):
    # scp = StoreSCP(args)
    scp = FindSCP()

if '__main__' == __name__:
    main(['moc_scp.py', '11112'])
