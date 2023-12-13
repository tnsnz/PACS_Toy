from pynetdicom import (
    AE,
    evt,
    debug_logger,
    AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES,
    events
)
from pynetdicom.sop_class import CTImageStorage

from filemanager import FileManager

debug_logger()


class FindSCP:
    def __init__(self):
        pass


class StoreSCP:
    def __init__(self):
        ae = AE()
        ae.acse_timeout = 5
        ae.dimse_timeout = 5
        ae.network_timeout = 5
        ae.add_supported_context(CTImageStorage)

        for cx in AllStoragePresentationContexts:
            ae.add_supported_context(cx.abstract_syntax, ALL_TRANSFER_SYNTAXES)

        handlers = [(evt.EVT_C_STORE, self.handle_store)]

        ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)

    def handle_store(self, event: events.Event):
        dataset_binary = event.request.DataSet.getvalue()
        stored = FileManager().store(event.dataset, dataset_binary, event.file_meta)

        if stored:
            return 0xFF00
        else:
            return 0xC000


class GetSCP:
    def __init__(self):
        pass


s = StoreSCP()
