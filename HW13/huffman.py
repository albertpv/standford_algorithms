'''
In this programming problem and the next you'll code up the greedy algorithm from the lectures on
Huffman coding.

The huffman_coding.txt file describes an instance of the problem. It has the following format:
[number_of_symbols]
[weight of symbol #1]
[weight of symbol #2]
...

For example, the third line of the file is "6852892," indicating that the weight of the second
symbol of the alphabet is 6852892. (We're using weights instead of frequencies, like in the "A
More Complex Example" video.)

Your task in this problem is to run the Huffman coding algorithm from lecture on this data set.
What is the maximum length of a codeword in the resulting Huffman code?
'''
import time
import sys


# Binary Search Tree class (all nodes have non-NULL values, preserves left/right props of BST)
class Binary_Search_Tree:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    def insert(self, val):
        if self.val is None:
            self.val = val
        else:
            self._insert(val, self)

    def _insert(self, val, root):
        if val < root.val:
            if root.left is None:
                root.left = Binary_Search_Tree(val)
            else:
                self._insert(val, root.left)
        else:
            if root.right is None:
                root.right = Binary_Search_Tree(val)
            else:
                self._insert(val, root.right)

    def contains(self, val):
        if self.val is None:
            return None
        else:
            return self._contains(val, self)

    def _contains(self, val, root):
        if val == root.val:
            return True
        elif val < root.val and root.left is not None:
            return self._contains(val, root.left)
        elif val > root.val and root.right is not None:
            return self._contains(val, root.right)
        else:
            return False

    def get_root(self):
        return self.val

    def print_tree(self, tree):
        if tree is not None:
            self.print_tree(tree.left)
            print(tree.val)
            self.print_tree(tree.right)

    def delete_tree(self):
        self.val = None
        self.left = None
        self.right = None


# Binary Tree class (nodes can have any values, not "ordered" overall like BST)
# Note: 0 is placeholder value for interior nodes
class Binary_Tree:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None

    def insert(self, val, children):
        self.val = val
        self.right = Binary_Tree(children[0])
        self.left = Binary_Tree(children[1])

    # finds the target node (sum of summands) and splits it
    def split(self, root, summand_1, summand_2, found=False):
        if found is True:
            return True
        if root.val == summand_1 + summand_2:
            root.insert(0, [summand_1, summand_2])
            return True
        elif root.left is not None:
            found = self.split(root.left, summand_1, summand_2, found)
            found = self.split(root.right, summand_1, summand_2, found)

    # uses Huffman binary tree to generate encodings for all characters
    def gen_huffman_codes(self, root, curr_code=[]):
        if root.val is not 0:
            Char_Codes[root.val] = curr_code.copy()
            curr_code.pop()
        elif root.left is not None:
            curr_code.append(0)
            curr_code = self.gen_huffman_codes(root.left, curr_code)
            curr_code.append(1)
            curr_code = self.gen_huffman_codes(root.right, curr_code)
            if curr_code:
                curr_code.pop()
        return curr_code

    def print_tree(self, tree):
        if tree is not None:
            self.print_tree(tree.left)
            print(tree.val)
            self.print_tree(tree.right)


# Heap class
# input: order is 0 for max heap, 1 for min heap
class Heap():
    def __init__(self, order=1):
        self._heap = []
        self._min_heap = order

    def __str__(self):
        output = '['
        size = len(self._heap)
        for i, v in enumerate(self._heap):
            txt = ', ' if i is not size - 1 else ''
            output += str(v) + txt
        return output + ']'

    # input: parent and child nodes
    def _is_balanced(self, p, c):
        is_min_heap = p <= c
        return is_min_heap if self._min_heap else not is_min_heap

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    # input: parent and child indices
    def _sift_up(self, p_i, c_i):
        if p_i == -1:
            return
        p = self._heap[p_i]
        c = self._heap[c_i]
        while (not self._is_balanced(p, c)):
            p_i = (c_i - 1) // 2
            self._swap(c_i, p_i)

            c_i = p_i
            if c_i is 0:
                break
            p = self._heap[(c_i - 1) // 2]

    # input: parent and child indices
    def _sift_down(self, p_i, c_i):
        while (c_i and not self._is_balanced(self._heap[p_i], self._heap[c_i])):
            self._swap(p_i, c_i)
            p_i = c_i
            c_i = self._get_swapped_child_index(p_i)

    def get_root(self):
        if self._heap:
            return self._heap[0]

    def get_nodes(self):
        return self._heap

    # inserts node in O(logn) time
    def insert(self, node):
        self._heap.append(node)
        node_i = len(self._heap) - 1
        self._sift_up((node_i - 1) // 2, node_i)

    # input: parent index
    # output: index of smaller or greater child, one index if other DNE, or None
    def _get_swapped_child_index(self, p_i):
        size = len(self._heap)
        i = p_i * 2 + 1
        j = p_i * 2 + 2
        if size <= i:
            return None
        elif size <= j:
            return i

        if self._heap[i] > self._heap[j]:
            return j if self._min_heap else i
        else:
            return i if self._min_heap else j

    def _extract_root(self):
        if self._heap:
            self._swap(0, len(self._heap) - 1)
            root = self._heap.pop()
            self._sift_down(0, self._get_swapped_child_index(0))
            return root

    # extracts minimum value in O(logn) time
    def extract_min(self):
        if not self._min_heap:
            raise ValueError('Only min heaps support extract_min')
        return self._extract_root()

    # extracts maximum value in O(logn) time
    def extract_max(self):
        if self._min_heap:
            raise ValueError('Only max heaps support extract_max.')
        return self._extract_root()

    # deletes node from anywhere in heap in O(logn) time
    # input: key (i.e. index) of node to delete
    def delete(self, key):
        self._swap(key, len(self._heap) - 1)
        removed = self._heap.pop()

        p_i = (key - 1) // 2
        if not self._is_balanced(self._heap[p_i], self._heap[key]):
            self._sift_up(p_i, key)
        else:
            self._sift_down(p_i, key)

        return removed

    # initializes a heap in O(n) time
    def heapify(self):  # to do
        return self._heap


# Global variables
H = Heap()  # keys: frequencies, values: node labels
B = Binary_Tree()
Merge_Record = []
Char_Codes = {}


def populate_heap(filename):
    with open(filename) as f_handle:
        num_chars = int(f_handle.readline())
        if num_chars <= 2:
            return
        for line in f_handle:
            char_wt = int(line)
            H.insert(char_wt)


# output: binary tree of huffman codes
def gen_huffman_binary_tree():
    global H, B, Merge_Record

    nodes = H.get_nodes()
    if len(nodes) == 2:
        B.insert(0, nodes)
    else:
        # replace 2 smallest-frequency nodes with meta-node
        min_1, min_2 = H.extract_min(), H.extract_min()
        meta_node = min_1 + min_2
        H.insert(meta_node)
        Merge_Record += [min_1, min_2]  # least to greatest

        gen_huffman_binary_tree()

        # Splits meta-node previously almagamated on this iteration from 2 smallest frequences
        max_1, max_2 = Merge_Record.pop(), Merge_Record.pop()
        B.split(B, max_1, max_2)


def get_min_max_code_lengths():
    char_code_lengths = {k: len(v) for k, v in Char_Codes.items()}
    return min(char_code_lengths.values()), max(char_code_lengths.values())


def main():
    start = time.time()
    sys.setrecursionlimit(800000)

    populate_heap('huffman.txt')
    gen_huffman_binary_tree()
    B.gen_huffman_codes(B)

    # expected '_ex' file results: min length = 2, max length = 5
    print('min length, max length: ', get_min_max_code_lengths())
    print('elapsed time: ', time.time() - start)


main()