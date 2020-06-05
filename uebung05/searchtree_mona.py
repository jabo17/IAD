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
        #key ist nichts
        if key is None:
            return None
        #found key:    
        if key == self._root._key:
            return self._root._value
        #key must be in left tree, because of tree structure
        if key < self._root._key:
            return self._root._left[key]
        #key must be in right tree
        if key > self._root._key:
            return self._root._right[key]
        #now key cant exist in the tree
        return None    

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        #key is nothing
        if key is None:
            raise KeyError("None can't be set!")
        #end of recursion: we found the right place for key
        if self._root is None: 
            self._root._key = key
            self._root._value = value
            self._size += 1
        #key already exists: replace old value for current
        if key == self._root._key:
            self._root._value = value
        #key must be set in left tree
        if key < self._root._key:
            self._root._left = self._root._left.__setitem__(key,value)
        #key must be set in right tree
        if key > self._root._key:
            self._root._right = self._root._right.__setitem__(key, value)
        return self
    
    def tree_predecessor (self):
        node = self._root._left
        while self._root._right is not None:
            node = self._root._right
        return node 

    def __delitem__(self, key):          # implements 'del tree[key] '
        #key is nothing
        if key is None:
            raise KeyError("key is not set in this tree")
        if key < self._root._key:
            #key must be in left tree
            self._root._left = self._root._left.__delitem__ (key)
        if key > self._root._key:
            #key must be in right tree
            self._root._right = self._root._right.__delitem__ (key)
        else: 
            #now key must be self._root
            if self._root._left is None and self._root._right is None:
                #Node is a leaf node (Blatt)
                self._root._value = None
                self._root._key = None
                self._size -= 1
            #Node has one child:
            elif self._root._left is None: 
                self._root = self._root._right
                self._size -= 1
            elif self._root._right is None:
                self._root = self._root._left
                self._size -= 1
            #node has two children:
            else:
                pred = self.tree_predecessor()
                self._root._key = pred._key
                self._root._key = pred._value
                self._root._left = self._root._left.__delitem__(pred._key)
                self._size -= 1
            return self 


    @staticmethod
    def _tree_find(node, key):           # internal implementation
        ... # your code here

    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        ... # your code here

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        ... # your code here

def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    
    ... # your code here
