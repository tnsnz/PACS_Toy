from pydicom import Dataset

from trees import *


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

        self.modality = ''
        self.modality_valid = False

        self.decode(ds)

    def decode(self, ds: Dataset):
        if hasattr(ds, 'PatientID'):
            self.p_id_valid = True
            self.p_id = ds.PatientID

        if hasattr(ds, 'PatientName'):
            self.p_name_valid = True
            self.p_name = ds.PatientName.alphabetic
            # self.p_name = ds.PatientName.original_string.decode()

        if hasattr(ds, 'StudyID'):
            self.s_id_valid = True
            self.s_id = ds.StudyID

        if hasattr(ds, 'SeriesNumber'):
            self.s_num_valid = True
            self.s_num = ds.SeriesNumber.original_string

        if hasattr(ds, 'Modality'):
            self.modality_valid = True
            self.modality = ds.Modality

    def is_valid_to_store(self):
        return self.p_id_valid and self.p_name_valid and self.s_id_valid and self.s_num_valid and self.modality_valid

    def is_valid_to_find_patient(self):
        return self.p_id_valid or self.p_name_valid

    def is_valid_to_find_study(self):
        return self.s_id_valid

    def is_valid_to_find_series(self):
        return self.s_num_valid

    def patient_path(self):
        return self.p_name + '_' + self.p_id


class DatasetEncoder:
    def __init__(self, tree_node: TreeNode):
        self.__ds = Dataset()
        self.read_tree(tree_node)

    def read_tree(self, tree_node: TreeNode):
        if tree_node == tree_node.get_root():
            return

        if isinstance(tree_node, SeriesTreeNode):
            self.__ds.SeriesNumber = tree_node.get_id()
        elif isinstance(tree_node, StudyTreeNode):
            self.__ds.StudyID = tree_node.get_id()
        elif isinstance(tree_node, PatientTreeNode):
            self.__ds.PatientID = tree_node.get_id()
            self.__ds.PatientName = tree_node.get_name()

        self.read_tree(tree_node.get_parent())

    def get_dataset(self):
        return self.__ds
