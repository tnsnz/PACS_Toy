import _io
import os
from typing import List, Dict, Set

from pydicom import Dataset
from pydicom.filewriter import write_file_meta_info

from dataset_decoder import DatasetDecoder
from singleton import Singleton

# find patient information from server
# file structure is structured as follows
'''
- Server base dir
  └ {PatientName}_{PatientID}
    └ study_{StudyID_1}
      └ series_{SeriesNumber_1}
        └ {Modality}
        └ ...
      └ ...
      └ series_{SeriesNumber_n}
        └ {Modality}
        └ ...
    └ ...
    └ study_{StudyID_n}
  └ ...  
  └ {PatientName}_{PatientID}
'''

base_storage_dir = 'store_dir'

study_concat = 'study_'
series_concat = 'series_'
f_concat = '_'
d_concat = '/'


class LocalStorage:
    def __init__(self):
        self.base_storage_path = 'store_dir'  # DBManager.get_base_storage_path()

        self.patient_id: Dict[str, Set[str]] = {}
        self.id_patient: Dict[str, str] = {}

        self.name_study: Dict[str, Set[str]] = {}
        self.id_study: Dict[str, Set[str]] = {}

        self.study_series: Dict[str, Set[str]] = {}

        # self.initiate()


class FileManager(object, metaclass=Singleton):
    def __init__(self):
        self.local_storage = LocalStorage()
        self.candidates: List[str] = []
        self.target_dir = ''

    def create_directory(self, target_dir, ds: DatasetDecoder):
        try:
            os.makedirs(base_storage_dir, exist_ok=True)

            patient_folder_name = ds.p_name + f_concat + ds.p_id
            patient_folder_dir = base_storage_dir + d_concat + patient_folder_name
            os.makedirs(patient_folder_dir, exist_ok=True)

            study_folder_name = study_concat + ds.s_id
            study_folder_dir = patient_folder_dir + d_concat + study_folder_name
            os.makedirs(study_folder_dir, exist_ok=True)

            series_folder_name = series_concat + ds.s_num
            series_folder_dir = study_folder_dir + d_concat + series_folder_name
            os.makedirs(series_folder_dir, exist_ok=True)

            self.target_dir = series_folder_dir
        except Exception as e:
            print(e)

    def store(self, ds: Dataset, dataset_binary: bytes, file_meta):
        stored = False
        decoded_ds = DatasetDecoder(ds)

        if not decoded_ds.can_store():
            return stored

        self.target_dir = ''
        self.create_directory(self.target_dir, decoded_ds)
        file_path = self.target_dir + d_concat + ds.SOPInstanceUID
        print(file_path)
        try:
            with open(file_path, 'wb') as f:
                f.write(b'\x00' * 128)
                f.write(b'DICM')
                write_file_meta_info(f, file_meta)
                f.write(dataset_binary)
                stored = True
        except Exception as e:
            print(e)

        return stored
