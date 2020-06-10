import pytest

class SearchTree:
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None

    def __init__(self):
        self._root = None
        self._size = 0
        
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):          # implements 'value = tree[key]'
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError("key not found")
        return node._value

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            self._size += 1
        self._root = SearchTree._tree_insert(self._root, key, value)

    def __delitem__(self, key):          # implements 'del tree[key] '
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError("key not found")
        self._size -= 1
        self._root = SearchTree._tree_remove(self._root, key)

    # 5b
    def depth(self):
        return SearchTree._tree_depth(self._root, self._size)[0]

    # part of 5b (internal implementation)
    # @params node where to begin, >= max Elements that can be visited
    # @return maxPath and visted elements
    # visted elements helps us to earlier recognize the maxpath and futhermore to prevent more recursion
    @staticmethod
    def _tree_depth(node, elements):
        if node is None:
            return 0, 0
        leftMax, elLeft = SearchTree._tree_depth(node._left, elements-1)

        #falls wahr, ist rechts keine längerer Pfad mehr
        if leftMax >= elements-1-elLeft:
            return leftMax+1, elements-1-elLeft

        rightMax, elRight = SearchTree._tree_depth(node._right, elements -1 -elLeft)

        if leftMax < rightMax:
            return rightMax+1, elLeft+elRight+1
        else:
            return leftMax+1, elLeft+elRight+1

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        if node is None:
            return None
        if node._key == key:
            return node
        if key < node._key:
            return SearchTree._tree_find(node._left, key)
        else:
            return SearchTree._tree_find(node._right, key)

    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        if node is None:
            return SearchTree.Node(key, value)
        if node._key == key:
            node._value = value
            return node
        elif key < node._key:
            node._left = SearchTree._tree_insert(node._left, key, value)
        else:
            node._right = SearchTree._tree_insert(node._right, key, value)
        return node

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        if node is None:
            return None
        if key < node._key:
            node._left = SearchTree._tree_remove(node._left, key)
        elif key > node._key:
            node._right = SearchTree._tree_remove(node._right, key)
        else:
            if node._left is None and node._right is None:
                node = None
            elif node._left is None:
                node = node._right
            elif node._right is None:
                node = node._left
            else:
                pred = SearchTree._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._left = SearchTree._tree_remove(node._left, pred._key)
        return node
    
    @staticmethod
    def _tree_predecessor(node):
        pred = node._left
        while pred._right is not None:
            pred = pred._right
        return pred


def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    
    t[0] = "A"
    assert t.depth() == 1
    assert t._root._key == 0
    t[1] = "B"
    assert t._root._right._key == 1
    assert t.depth() == 2
    t[2] = "C"
    t[3] = "D"
    t[4] = "E"
    t[-1] = "F"

    assert t.depth() == 5
    assert t._size == 6

    assert t[-1] == "F"
    del t[-1]
    assert t._size == 5
    assert t.depth() == 5


# Aufgabe c)
# am besten immer das median von keys hinzufügen, dann Liste der keys beim median splitten, und von den Teilslisten das median hinzufügen

# Aufgabe d)
# TODO