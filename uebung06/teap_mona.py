from searchtreeclass import SearchTree
import random

class RandomTreap(SearchTree):
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None
            #TODO selbe Zufallszahl?
            self._priority= random.random()
    
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
        if node._left._priority > node._priority:
            node = RandomTreap._tree_rotate_right(node._left)
        elif node._right._priority > node._priority:
            node = RandomTreap._tree_rotate_left(node._right)
        return node
 