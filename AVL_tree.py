from BST import *
import random


class AVLTreeNode(BinaryTreeNode):

    def __init__(self, data):
        self.height = 0
        super().__init__(data)

    def calc_height(self):
        self.height = max(self.child_heights) + 1

    @property
    def child_heights(self):
        if self.left_child is None:
            left_height = -1
        else:
            left_height = self.left_child.height
        if self.right_child is None:
            right_height = -1
        else:
            right_height = self.right_child.height
        return left_height, right_height


class AVLTree(BinarySearchTree):

    def calc_heights_after_rotation(self, new_sub_root):
        if new_sub_root.left_child is not None:
            new_sub_root.left_child.calc_height()
        if new_sub_root.right_child is not None:
            new_sub_root.right_child.calc_height()
        new_sub_root.calc_height()

    def right_rotation(self, sub_root):
        new_sub_root = sub_root.left_child
        temp = new_sub_root.right_child

        new_sub_root.right_child = sub_root
        sub_root.left_child = temp

        self.calc_heights_after_rotation(sub_root)
        self.calc_heights_after_rotation(new_sub_root)

        return new_sub_root

    def left_rotation(self, sub_root):
        new_sub_root = sub_root.right_child
        temp = new_sub_root.left_child

        new_sub_root.left_child = sub_root
        sub_root.right_child = temp

        self.calc_heights_after_rotation(sub_root)
        self.calc_heights_after_rotation(new_sub_root)

        return new_sub_root

    def _insert(self, data, sub_root):
        if sub_root is None:
            self._size += 1
            return AVLTreeNode(data)
        sub_root = super()._insert(data, sub_root)
        sub_root = self._rotate_if_needed(sub_root)
        return sub_root

    def _remove(self, data, sub_root):
        sub_root = super()._remove(data, sub_root)
        sub_root = self._rotate_if_needed(sub_root)
        return sub_root

    def _rotate_if_needed(self, node):
        if node is None:
            return node
        node.calc_height()
        (left_height, right_height) = node.child_heights
        if left_height - right_height > 1:
            # Right Rotation Needed
            if node.left_child is not None:
                (left_height, right_height) = \
                    node.left_child.child_heights
                if right_height - left_height > 0:
                    # Left Right Rotation Needed
                    node.left_child = self.left_rotation(node.left_child)
            node = self.right_rotation(node)
        elif right_height - left_height > 1:
            # Left Rotation Needed
            if node.right_child is not None:
                (left_height, right_height) = \
                    node.right_child.child_heights
                if left_height - right_height > 0:
                    # Right Left Rotation Needed
                    node.right_child = self.right_rotation(node.right_child)
            node = self.left_rotation(node)
        return node

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


def check_AVL_cond(sub_root):
    if sub_root is not None:
        (left, right) = sub_root.child_heights
        if abs(left-right) > 1:
            print("AVL Violated")
        if sub_root.left_child is not None:
            check_AVL_cond(sub_root.left_child)
        if sub_root.right_child is not None:
            check_AVL_cond(sub_root.right_child)


my_tree = AVLTree()
random.seed(1)
for _ in range(1000):
    num = random.randint(0, 1000)
    print("inserting", num)
    my_tree.insert(num)
    check_AVL_cond(my_tree._root)
print("\nNew Tree:")
my_tree.print_tree()

for _ in range(4000):
    num = random.randint(0, 1000)
    print("Removing", num)
    try:
        my_tree.remove(num)
        print("Removed")

    except AVLTree.NotFoundError:
        pass
        print("Not Found")
    check_AVL_cond(my_tree._root)

print("New Tree:")
my_tree.print_tree()