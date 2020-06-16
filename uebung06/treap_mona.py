from searchtreeclass import SearchTree
import random
 

class RandomTreap(SearchTree):

    class Node(SearchTree.Node):
        def __init__(self, key, value,priority):
            self._key = key
            self._value = value
            self._left = self._right = None
            self._priority= random.random()
    
    def __init__(self):
        self._root = None
        self._size = 0
    
    def priority(self):
        return RandomTreap._root._priority
    
    def key(self):
        return self._root._key

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        node = RandomTreap._tree_find(self._root, key)
        if node is None:
            self._size += 1
        self._root = RandomTreap._tree_insert(self._root, key, value)

    @staticmethod
    def _tree_insert(node, key, value):
        #wie kann ich auf Vaterknoten zugreifen?
        if node is None:
            return SearchTree.Node(key, value)
        if node._key == key:
            node._value = value
            #DynamicTreap
            # node._priority+=1
            # node = RandomTreap._check_parent_root
            return node
        elif key < node._key:
            node._left = SearchTree._tree_insert(node._left, key, value)
        else:
            node._right = SearchTree._tree_insert(node._right, key, value)
        #check parent root
        node = RandomTreap._check_parent_root(node)
        return node
        

    @staticmethod
    def _check_parent_root(node):
        if node._left is None:
            return node
        if node._right is None:
            return node
        if node._left._priority > node._priority:
            node = RandomTreap._tree_rotate_right(node._left)
        elif node._right._priority > node._priority:
            node = RandomTreap._tree_rotate_left(node._right)
        return node
    
    #Rotation
    @staticmethod
    def _tree_rotate_right(old_root):
        new_root = old_root.left
        old_root.left = new_root.right
        new_root.right = old_root
        return new_root
    
    @staticmethod
    def _tree_rotate_left(old_root):
        new_root = old_root.right
        old_root.right = new_root.left
        new_root.left = old_root
        return new_root
    
    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        if node is None:
            return None
        if key < node._key:
            node._left = RandomTreap._tree_remove(node._left, key)
        elif key > node._key:
            node._right =RandomTreap._tree_remove(node._right, key)
        else:
            if node._left is None and node._right is None:
                node = None
            elif node._left is None:
                node = node._right
            elif node._right is None:
                node = node._left
            else:
                pred = RandomTreap._tree_predecessor(node)
                node._priority = pred._priority
                node._key = pred._key
                node._value = pred._value
                node._left = RandomTreap._tree_remove(node._left, pred._key)
                #check parent root
                node = RandomTreap._check_parent_root(node)
        return node
    
    #for DynamucTreap
    # @staticmethod
    # def _tree_find(node, key):           # internal implementation
    #     if node is None:
    #         return None
    #     if node._key == key:
    #         node._priority +=1
    #         return node
    #     if key < node._key:
    #         return SearchTree._tree_find(node._left, key)
    #     else:
    #         return SearchTree._tree_find(node._right, key)
    

def test_search_tree():
    t = RandomTreap()
    assert len(t) == 0
    
    t[0] = "A"
    assert t.depth() == 1
    assert t._root._key == 0
    t[1] = "B"
    assert t._root._right._key == 1
    assert t.depth() == 2
    assert t._root._priority > t._root._right._priority 
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

#main
t = RandomTreap()
len(t) == 0
                
t[0] = "A"
t.key()

t[1] = "B"
t.priority()
                
    
    