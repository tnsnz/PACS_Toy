import os
from typing import Set

from dataset_handler import DatasetDecoder, DatasetEncoder
from trees import *


class LocalStorage:
    def __init__(self):
        self.root = TreeNode('store_dir')
        self.id_name: Dict[str, str] = dict()
        self.name_id: Dict[str, Set[str]] = dict()

        self.p_name_nodes: Dict[str, Set[TreeNode]] = dict()
        self.p_id_nodes: Dict[str, TreeNode] = dict()
        self.patient_nodes: Dict[str, TreeNode] = dict()
        self.study_nodes: Dict[str, Set[TreeNode]] = dict()
        self.series_nodes: Dict[str, Set[TreeNode]] = dict()

        self.initiate()

    def initiate(self):
        self.initiate_patient()

    def find_matched_dirs(self, ds: DatasetDecoder, level: str):
        ret = []

        cond_level = level.upper()

        candidates: List[TreeNode] = []
        patient_candidates: List[TreeNode] = []
        study_candidates: List[TreeNode] = []
        series_candidates: List[TreeNode] = []

        if ds.is_valid_to_find_patient():
            patient_candidates = self.get_matched_nodes(ds.p_id, ds.p_name)
        if ds.is_valid_to_find_study():
            study_candidates = list(self.study_nodes[ds.s_id])
        if ds.is_valid_to_find_series():
            series_candidates = list(self.series_nodes[ds.s_num])

        if 'PATIENT' == cond_level:
            candidates = patient_candidates
        elif 'STUDY' == cond_level and ds.is_valid_to_find_study():
            candidates = pruning_nodes(study_candidates, patient_candidates)
        elif 'SERIES' == cond_level:
            matched_study = set(pruning_nodes(series_candidates, study_candidates))
            matched_patient = set(pruning_nodes(series_candidates, patient_candidates))
            if 0 < len(matched_study) and 0 < len(matched_patient):
                candidates = list(matched_patient.union(matched_study))
            elif 0 < len(matched_study):
                candidates = list(matched_study.union(series_candidates))
            elif 0 < len(patient_candidates):
                candidates = list(matched_patient.union(series_candidates))
            else:
                candidates = series_candidates

        for candidate in candidates:
            ret.append(DatasetEncoder(candidate).get_dataset())

        return ret

    def get_matched_nodes(self, p_id: str, p_name: str) -> List[TreeNode]:
        ret = []

        if '' != p_id and '' != p_name:
            ret.append(self.patient_nodes[p_name + '_' + p_id])
        elif '' != p_id:
            ret.append(self.p_id_nodes[p_id])
        else:
            ret = list(self.p_name_nodes[p_name])

        return ret

    def initiate_patient(self):
        root_name = self.root.get_id()
        for p_name_id in os.listdir(root_name):
            p_name, p_id = p_name_id.split('_')

            p_node = PatientTreeNode(p_name, p_id, self.root)

            self.name_id.setdefault(p_name, set())
            self.name_id[p_name].add(p_id)
            self.id_name[p_id] = p_name
            self.p_name_nodes.setdefault(p_name, set())
            self.p_name_nodes[p_name].add(p_node)
            self.p_id_nodes[p_id] = p_node
            self.patient_nodes[p_node.get_full_id()] = p_node
            self.initiate_study(p_node)

    def initiate_study(self, patient_node: PatientTreeNode):
        patient_path = patient_node.to_string()
        for study_id in os.listdir(patient_path):
            study_node = StudyTreeNode(study_id, parent=patient_node)
            study_id = study_node.get_id()
            self.study_nodes.setdefault(study_id, set())
            self.study_nodes[study_id].add(study_node)
            self.initiate_series(study_node)

    def initiate_series(self, study_node: StudyTreeNode):
        study_path = study_node.to_string()
        for series_num in os.listdir(study_path):
            series_node = SeriesTreeNode(series_num, parent=study_node)
            series_num = series_node.get_id()
            self.series_nodes.setdefault(series_num, set())
            self.series_nodes[series_num].add(series_node)
            self.initiate_modality(series_node)

    def initiate_modality(self, series_node: SeriesTreeNode):
        series_path = series_node.to_string()
        for modality in os.listdir(series_path):
            TreeNode(modality, series_node)
            TreeNode(modality, series_node)

# from pydicom import Dataset
#
# ls = LocalStorage()
# ds = Dataset()
# ds.PatientName = 'Anonymous'
# ds.PatientID = '123456'
# ds.StudyID = 'SLICER10001'
# ds.SeriesNumber = '11'
# print(ls.find_matched_dirs(DatasetDecoder(ds), 'SERIES'))
