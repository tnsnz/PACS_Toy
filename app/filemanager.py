import os
from typing import List, Dict, Set, Union

from pydicom import Dataset

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

    def read_preamble(self, filename):
        with open(filename, 'rb') as fp:
            fp.read(128)  # preamble
            return fp.read(4) == b"DICM"

    def is_dicom(self, filepath: Union[str, List[str]]) -> bool:
        dicom = True
        if isinstance(filepath, str):
            if not self.read_preamble(filepath):
                dicom = False
        elif isinstance(filepath, list):
            for filename in filepath:
                if not self.read_preamble(filename):
                    dicom = False
                    break

        return dicom

    def get_dicom_files(self, fpaths):
        dicom_files = []
        files = self.get_files(fpaths)
        for file in files[0]:
            if self.is_dicom(file):
                dicom_files.append(file)

        return dicom_files

    def get_files(self, fpaths, recurse=False):
        out = []
        bad = []
        for fpath in fpaths:
            if os.path.isfile(fpath):
                out.append(fpath)
            elif os.path.isdir(fpath):
                if recurse:
                    for root, dirs, files in os.walk(fpath):
                        out += [os.path.join(root, pp) for pp in files]
                else:
                    out += [os.path.join(fpath, pp) for pp in os.listdir(fpath)]
            else:
                bad.append(fpath)

        return sorted(list(set([pp for pp in out if os.path.isfile(pp)]))), bad

    def create_directory(self, ds: DatasetDecoder):
        try:
            patient_folder_name = ds.p_name + f_concat + ds.p_id
            patient_folder_dir = base_storage_dir + d_concat + patient_folder_name

            study_folder_name = study_concat + ds.s_id
            study_folder_dir = patient_folder_dir + d_concat + study_folder_name

            series_folder_name = series_concat + ds.s_num
            series_folder_dir = study_folder_dir + d_concat + series_folder_name

            target_dir = series_folder_dir + d_concat + ds.modality
            os.makedirs(target_dir, exist_ok=True)

            return target_dir
        except Exception as e:
            print(e)

    def target_file(self, decoded_ds: DatasetDecoder, sop_uid):
        if not decoded_ds.can_store():
            return ''

        target_dir = self.create_directory(decoded_ds)
        filename = target_dir + d_concat + sop_uid
        return filename

    def deflated_store(self, filename: str, ds: Dataset, dataset_binary):
        try:
            with open(filename, "wb") as f:
                f.write(dataset_binary)
        except (OSError, Exception) as e:
            print(filename, e)
            raise e

    def store(self, filename: str, ds: Dataset):
        try:
            ds.save_as(filename, write_like_original=False)
        except (OSError, Exception) as e:
            print(filename, e)
            raise e
