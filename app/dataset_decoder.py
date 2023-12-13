from pydicom import Dataset


class DatasetDecoder:
    def __init__(self, ds: Dataset):
        # patient id
        self.p_id = ''
        self.p_id_valid = False
        # patient name
        self.p_name = ''
        self.p_name_valid = False
        # study id
        self.s_id = ''
        self.s_id_valid = False
        # series number
        self.s_num = ''
        self.s_num_valid = False

        self.decode(ds)

    def decode(self, ds: Dataset):
        if hasattr(ds, 'PatientID'):
            self.p_id_valid = True
            self.p_id = ds.PatientID

        if hasattr(ds, 'PatientName'):
            self.p_name_valid = True
            self.p_name = ds.PatientName.original_string.decode()

        if hasattr(ds, 'StudyID'):
            self.s_id_valid = True
            self.s_id = ds.StudyID

        if hasattr(ds, 'SeriesNumber'):
            self.s_num_valid = True
            self.s_num = ds.SeriesNumber.original_string

    def can_store(self):
        print(self.s_num_valid)
        return self.p_id_valid and self.p_name_valid and self.s_id_valid and self.s_num_valid

    def patient_path(self):
        return self.p_name + '_' + self.p_id
