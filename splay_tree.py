from BST import BinarySearchTree, BinaryTreeNode


class SplayTree(BinarySearchTree):
    def __init__(self):
        super().__init__()

    def insert(self, data):
        if self._root is None:
            self._root = BinaryTreeNode(data)
            self._size += 1
            return True
        self._root = self._splay(data)
        if data < self._root.data:
            new_node = BinaryTreeNode(data)
            new_node.left_child = self._root.left_child
            new_node.right_child = self._root
            self._root.left_child = None
            self._root = new_node
            self._size += 1
            return True
        elif data > self._root.data:
            new_node = BinaryTreeNode(data)
            new_node.left_child = self._root
            new_node.right_child = self._root.right_child
            self._root.right_child = None
            self._root = new_node
            self._size += 1
            return True
        else:
            return False

    def remove(self, data):
        if self._root is None:
            return False
        self._root = self._splay(data)
        if data != self._root.data:
            return False
        if self._root.left_child is None:
            new_root = self._root.right_child
        else:
            new_root = self._root.left_child
            new_root = self._splay(data, new_root)
            new_root.right_child = self._root.right_child
        self._root = new_root
        self._size -= 1
        return True

    def __contains__(self, data):
        try:
            self.find(data)
            return True
        except self.NotFoundError:
            return False

    def find(self, data):
        if self._root is None:
            raise BinarySearchTree.NotFoundError
        self._root = self._splay(data)
        if self._root.data != data:
            raise BinarySearchTree.NotFoundError
        else:
            return self._root.data

    def show_root(self):
        if self._root is not None:
            return self._root.data

    def print_tree(self, sub_root=None):
        if sub_root is None:
            if self._root is None:
                return
            else:
                sub_root = self._root
        self._print_tree(sub_root, 0)

    def _print_tree(self, sub_root, depth):
        if sub_root is None:
            return
        for _ in range(depth):
            print("-", end="")
        print(sub_root.data)
        print("L")
        self._print_tree(sub_root.left_child, depth + 1)
        print("R")
        self._print_tree(sub_root.right_child, depth + 1)

    def _splay(self, data, sub_root=None):
        if sub_root is None:
            sub_root = self._root
        right_tree = None
        left_tree = None
        right_tree_min = None
        left_tree_max = None

        while sub_root.data != data:
            if data < sub_root.data:
                if sub_root.left_child is None:
                    break
                if data < sub_root.left_child.data:
                    sub_root = self._right_rotation(sub_root)
                    # sub_root = self._root
                    if sub_root.left_child is None:
                        break
                if right_tree is None:
                    right_tree = sub_root
                    right_tree_min = sub_root
                else:
                    # Specifically, it will be placed to the left of R's minimum node
                    right_tree_min.left_child = sub_root
                    right_tree_min = sub_root
                sub_root = sub_root.left_child
            elif data > sub_root.data:
                if sub_root.right_child is None:
                    break
                if data > sub_root.right_child.data:
                    sub_root = self._left_rotation(sub_root)
                    # sub_root = self._root
                    if sub_root.right_child is None:
                        break
                if left_tree is None:
                    left_tree = sub_root
                    left_tree_max = sub_root
                else:
                    # Feels infinite loopy
                    left_tree_max.right_child = sub_root
                    left_tree_max = sub_root
                sub_root = sub_root.right_child
            else:
                break

        if left_tree is not None:
            left_tree_max.right_child = sub_root.left_child
            sub_root.left_child = left_tree
        if right_tree is not None:
            right_tree_min.left_child = sub_root.right_child
            sub_root.right_child = right_tree

        return sub_root

    def _right_rotation(self, sub_root):
        # Identify the new sub_root and save to a temporary variable
        new_sub_root = sub_root.left_child

        # Move the node that would otherwise become the "middle node" to its new
        # position on the left side of the tree
        # Thus maneuver also makes space for the old sub_root
        sub_root.left_child = new_sub_root.right_child

        # Move the old sub_root to its position on the right of the new sub_root
        new_sub_root.right_child = sub_root

        return new_sub_root

    def _left_rotation(self, sub_root):
        # Identify the new sub_root and save to a temporary variable
        new_sub_root = sub_root.right_child

        # Move the node that would otherwise become the "middle node" to its new
        # position on the right side of the tree
        # Thus maneuver also makes space for the old sub_root
        sub_root.right_child = new_sub_root.left_child

        # Move the old sub_root to its position on the left of the new sub_root
        new_sub_root.left_child = sub_root

        return new_sub_root