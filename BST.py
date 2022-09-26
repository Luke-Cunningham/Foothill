class BinaryTreeNode:

    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None


class BinarySearchTree:

    class NotFoundError(Exception):
        pass

    class EmptyTreeError(Exception):
        pass

    def __init__(self):
        self._root = None
        self._size = 0

    @property
    def size(self):
        return self._size

    def find(self, key):
        return self._find(key, self._root)

    def _find(self, key, sub_root):
        if sub_root is None:
            raise BinarySearchTree.NotFoundError
        if key < sub_root.data:
            return self._find(key, sub_root.left_child)
        if sub_root.data < key:
            return self._find(key, sub_root.right_child)
        else:
            return sub_root.data

    def insert(self, data):
        old_size = self._size
        self._root = self._insert(data, self._root)
        return self._size != old_size

    def _insert(self, data, sub_root):
        if sub_root is None:
            self._size += 1
            return BinaryTreeNode(data)
        if data < sub_root.data:
            sub_root.left_child = self._insert(data, sub_root.left_child)
        if sub_root.data < data:
            sub_root.right_child = self._insert(data, sub_root.right_child)
        return sub_root

    def remove(self, data):
        self._root = self._remove(data, self._root)

    def _remove(self, data, sub_root):
        if sub_root is None:
            raise BinarySearchTree.NotFoundError
        if data < sub_root.data:
            sub_root.left_child = self._remove(data, sub_root.left_child)
        elif sub_root.data < data:
            sub_root.right_child = self._remove(data, sub_root.right_child)
        elif sub_root.left_child is not None and \
                sub_root.right_child is not None:
            sub_root.data = self._find_max(sub_root.left_child)
            sub_root.left_child = \
                self._remove(sub_root.data, sub_root.left_child)
        else:
            sub_root = sub_root.left_child if sub_root.left_child is not None \
                else sub_root.right_child
            self._size -= 1
        return sub_root

    def find_min(self):
        if self._root is None:
            raise BinarySearchTree.EmptyTreeError
        return self._find_min(self._root)

    def _find_min(self, sub_root):
        if sub_root.left_child is None:
            return sub_root.data
        return self._find_min(sub_root.left_child)

    def find_max(self):
        if self._root is None:
            raise BinarySearchTree.EmptyTreeError
        return self._find_max(self._root)

    def _find_max(self, sub_root):
        if sub_root.right_child is None:
            return sub_root.data
        return self._find_max(sub_root.right_child)

    def traverse(self, function):
        if self._root:
            self._traverse(function, self._root)

    def _traverse(self, function, sub_root):
        if sub_root.left_child:
            self._traverse(function, sub_root.left_child)
        function(sub_root)
        if sub_root.right_child:
            self._traverse(function, sub_root.right_child)
        return