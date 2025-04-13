class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

class BPlusTree:
    def __init__(self, max_keys=4):
        self.root = Node(is_leaf=True)
        self.max_keys = max_keys

    def _find_leaf(self, key, node=None):
        node = node or self.root
        if node.is_leaf:
            return node
        for i, item in enumerate(node.keys):
            if key < item:
                return self._find_leaf(key, node.children[i])
        return self._find_leaf(key, node.children[-1])

    def search(self, key):
        leaf = self._find_leaf(key)
        for i, item in enumerate(leaf.keys):
            if item == key:
                return leaf.children[i]  # Value is in children for leaf nodes
        return None

    def insert(self, key, value):
        leaf = self._find_leaf(key)
        self._insert_in_leaf(leaf, key, value)
        if len(leaf.keys) > self.max_keys:
            self._split_leaf(leaf)

    def _insert_in_leaf(self, leaf, key, value):
        if key in leaf.keys:
            index = leaf.keys.index(key)
            leaf.children[index] = value
        else:
            for i, item in enumerate(leaf.keys):
                if key < item:
                    leaf.keys.insert(i, key)
                    leaf.children.insert(i, value)
                    return
            leaf.keys.append(key)
            leaf.children.append(value)

    def _split_leaf(self, leaf):
        new_leaf = Node(is_leaf=True)
        mid = len(leaf.keys) // 2
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.children = leaf.children[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]

        if leaf == self.root:
            new_root = Node()
            new_root.keys = [new_leaf.keys[0]]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
        else:
            self._insert_in_parent(self.root, leaf, new_leaf, new_leaf.keys[0])

    def _insert_in_parent(self, current, left, right, key):
        if current.is_leaf or current.children[0].is_leaf:
            current.keys.append(key)
            current.children.append(right)
            current.keys.sort()
            i = current.keys.index(key)
            current.children = sorted(current.children, key=lambda x: x.keys[0])
            if len(current.keys) > self.max_keys:
                self._split_internal(current)
            return

        for i, child in enumerate(current.children):
            if child == left:
                current.keys.insert(i, key)
                current.children.insert(i + 1, right)
                if len(current.keys) > self.max_keys:
                    self._split_internal(current)
                return
            elif not child.is_leaf:
                self._insert_in_parent(child, left, right, key)

    def _split_internal(self, node):
        new_node = Node()
        mid = len(node.keys) // 2
        mid_key = node.keys[mid]

        new_node.keys = node.keys[mid+1:]
        new_node.children = node.children[mid+1:]

        node.keys = node.keys[:mid]
        node.children = node.children[:mid+1]

        if node == self.root:
            new_root = Node()
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            self._insert_in_parent(self.root, node, new_node, mid_key)
bpt = BPlusTree(max_keys=3)
bpt.insert(10, "A")
bpt.insert(20, "B")
bpt.insert(5, "C")
bpt.insert(6, "D")
bpt.insert(12, "E")
print(bpt.search(6))  # Output: "D"
print(bpt.search(15)) # Output: None

