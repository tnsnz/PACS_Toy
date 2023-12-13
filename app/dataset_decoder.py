from pydicom import Dataset


class DatasetDecoder:
    def __init__(self, ds: Dataset):
        # patient id
        self.p_id = ''
        # patient name
        self.p_name = ''
        # study id
        self.s_id = ''
        # series number
        self.s_num = ''

        self.decode(ds)

    def decode(self, ds: Dataset):
        if hasattr(self.ds, 'PatientID'):
            self.p_id = ds.PatientID

        if hasattr(self.ds, 'PatientName'):
            self.p_name = ds.PatientName.original_string.decode()

        if hasattr(self.ds, 'StudyID'):
            self.s_id = ds.StudyID

        if hasattr(self.ds, 'SeriesName'):
            self.s_num = ds.SeriesNumber.original_string
