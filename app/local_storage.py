from __future__ import annotations

import os
from typing import List, Dict, Set

from pydicom import Dataset

from dataset_decoder import DatasetDecoder


class TreeNode:
    def __init__(self, node_id: str, parent: TreeNode = None):
        self._node_id: str = node_id
        self._parent: TreeNode = parent
        self._children: Dict[str, TreeNode] = dict()

        if None is parent:
            self._root = self
        else:
            self._root: TreeNode = parent._root
            parent.add_child(self)

    def add_child(self, child):
        if child._parent is not self:
            child._parent = self
            child._root = self._root

        self._children[child._node_id] = child

    def find_child(self, node_id):
        return self._children.get(node_id)

    def get_id(self):
        return self._node_id

    def get_parent(self):
        return self._parent

    def get_root(self):
        return self._root

    def to_string(self):
        ret = ''
        parent = self
        while self._root != parent:
            ret = parent._node_id + '/' + ret
            parent = parent._parent

        return self._root._node_id + '/' + ret

    def find_leafs(self, leafs):
        if self.is_leaf():
            leafs.append(self)

        for child in self._children.values():
            child.find_leafs(leafs)

    def find_leaf_dirs(self, leafs):
        if self.is_leaf():
            leafs.append(self.to_string())

        for child in self._children.values():
            child.find_leaf_dirs(leafs)

    def is_leaf(self):
        return 0 == len(self._children)


class PatientTreeNode(TreeNode):
    def __init__(self, p_name: str, p_id: str, parent=None):
        super().__init__(p_name + '_' + p_id, parent)
        self._p_name = p_name
        self._p_id = p_id

    def get_name(self):
        return self._p_name

    def get_id(self):
        return self._p_id

    def get_full_id(self):
        return self._p_name + '_' + self._p_id


class SepTreeNode(TreeNode):
    def __init__(self, s_id: str, separator: str = '_', parent=None):
        super().__init__(s_id, parent)
        l, r = s_id.split(separator)

        self.concat = separator
        self._base_id = l
        self._id = r

    def get_id(self):
        return self._id

    def get_full_id(self):
        return self._base_id + '_' + self._id


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

    def can_node_pruning(self, node: TreeNode, parent_nodes: List[TreeNode]):
        return node.get_parent() in parent_nodes

    def lcs_match_with_parent_candidates(self, candidate: TreeNode, parent_candidates):
        matched = False
        if candidate.get_parent() == candidate.get_root():
            return matched

        if self.can_node_pruning(candidate, parent_candidates):
            matched = True
        else:
            matched = self.lcs_match_with_parent_candidates(candidate.get_parent(), parent_candidates)

        return matched

    def pruning_nodes(self, candidates: List, parent_candidates):
        ret = []
        for candidate in candidates:
            if self.lcs_match_with_parent_candidates(candidate, parent_candidates):
                ret.append(candidate)

        return ret

    def find_files_in_dataset(self, ds: DatasetDecoder, level: str):
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
            candidates = self.pruning_nodes(study_candidates, patient_candidates)
        elif 'SERIES' == cond_level:
            matched_patient = self.pruning_nodes(series_candidates, patient_candidates)
            candidates = self.pruning_nodes(matched_patient, study_candidates)

        for candidate in candidates:
            ret.append(candidate.to_string())

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
            study_node = SepTreeNode(study_id, parent=patient_node)
            study_id = study_node.get_id()
            self.study_nodes.setdefault(study_id, set())
            self.study_nodes[study_id].add(study_node)
            self.initiate_series(study_node)

    def initiate_series(self, study_node: SepTreeNode):
        study_path = study_node.to_string()
        for series_num in os.listdir(study_path):
            series_node = SepTreeNode(series_num, parent=study_node)
            series_num = series_node.get_id()
            self.series_nodes.setdefault(series_num, set())
            self.series_nodes[series_num].add(series_node)
            self.initiate_modality(series_node)

    def initiate_modality(self, series_node: SepTreeNode):
        series_path = series_node.to_string()
        for modality in os.listdir(series_path):
            TreeNode(modality, series_node)
            TreeNode(modality, series_node)


ls = LocalStorage()
ds = Dataset()
ds.PatientName = 'Anonymous'
ds.PatientID = '123456'
# ds.StudyID = 'SLICER10001'
ds.SeriesNumber = '1'
print(ls.find_files_in_dataset(DatasetDecoder(ds), 'SERIES'))
