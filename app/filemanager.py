from typing import List, Dict, Set

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


class LocalStorage:
    def __init__(self):
        self.base_storage_path = 'store_dir'  # DBManager.get_base_storage_path()

        self.patient_id: Dict[str, Set[str]] = {}
        self.id_patient: Dict[str, str] = {}

        self.name_study: Dict[str, Set[str]] = {}
        self.id_study: Dict[str, Set[str]] = {}

        self.study_series: Dict[str, Set[str]] = {}

        # self.initiate()


class FileManager:
    def __init__(self):
        self.local_storage = LocalStorage()

        self.concat = '_'
        self.candidates: List[str] = []

    def findSpeicificPath(self):
        pass

    def findPatientName(self):
        pass

    def findPatientID(self):
        pass

    def findStudyGroup(self):
        pass

    def findSeriesGroup(self):
        pass

    def request_find(self):
        pass
