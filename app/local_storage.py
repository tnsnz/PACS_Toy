import os
from typing import List, Dict


class TreeNode:
    def __init__(self, node_id: str, parent=None):
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

    def get_full_id(self):
        return self._base_id + '_' + self._id


class LocalStorage:
    def __init__(self):
        self.root = TreeNode('store_dir')
        self.initiate()

    def initiate(self):
        self.initiate_patient()

    def initiate_patient(self):
        root_name = self.root.get_id()
        print(root_name)
        for path_list in os.listdir(root_name):
            p_name, p_id = path_list.split('_')
            p_node = PatientTreeNode(p_name, p_id, self.root)
            self.initiate_study(p_node)

    def initiate_study(self, patient_node: PatientTreeNode):
        patient_path = patient_node.to_string()
        print(patient_path)
        for path_list in os.listdir(patient_path):
            study_node = SepTreeNode(path_list, parent=patient_node)
            self.initiate_series(study_node)

    def initiate_series(self, study_node: SepTreeNode):
        study_path = study_node.to_string()
        for path_list in os.listdir(study_path):
            series_node = SepTreeNode(path_list, parent=study_node)
            TreeNode('MR', series_node)
            TreeNode('CT', series_node)
