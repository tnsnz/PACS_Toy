from __future__ import annotations

from typing import Dict, List


def can_node_pruning(node: TreeNode, parent_nodes: List[TreeNode]):
    return node.get_parent() in parent_nodes


def lcs_match_with_parent_candidates(candidate: TreeNode, parent_candidates):
    matched = False
    if candidate.get_parent() == candidate.get_root():
        return matched

    if can_node_pruning(candidate, parent_candidates):
        matched = True
    else:
        matched = lcs_match_with_parent_candidates(candidate.get_parent(), parent_candidates)

    return matched


def pruning_nodes(candidates: List, parent_candidates):
    ret = []
    for candidate in candidates:
        if lcs_match_with_parent_candidates(candidate, parent_candidates):
            ret.append(candidate)

    return ret


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


class StudyTreeNode(SepTreeNode):
    def __init__(self, s_id: str, separator: str = '_', parent=None):
        super().__init__(s_id, separator, parent)


class SeriesTreeNode(SepTreeNode):
    def __init__(self, s_id: str, separator: str = '_', parent=None):
        super().__init__(s_id, separator, parent)
