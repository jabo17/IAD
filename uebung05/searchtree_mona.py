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
        node = SearchTree._tree_find(self._root,key)
        if node is None:
            raise KeyError("item does not exist")
        return node._value

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        node = SearchTree._tree_find(self._root, key)
        if node is None:    #node was not item of tree
            self._size += 1
        #self._root because the item needs to be linked to the tree
        #function returns root either way
        self._root = SearchTree._tree_insert(self._root, key, value)
    

    def __delitem__(self, key):          # implements 'del tree[key] '
        node = SearchTree._tree_find(self._root, key)
        if node is not None:
            self._size -= 1
        else:
            raise KeyError("key and node not found!")
        self._root= SearchTree._tree_remove(self._root,key)

    def depth(self, node):
        return node

    @staticmethod
    def _tree_depth_():
        return 5
        

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        if node is None:
            return None
        if key is None:
            return None
        #found key:    
        if key == node._key:
            return node
        #key must be in left tree, because of tree structure
        if key < node._key:
            return SearchTree._tree_find(node._left, key)
        #key must be in right tree
        if key > node._key:
            return SearchTree._tree_find(node._right, key)
        #now key cant exist in the tree
        return None  


    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        #key is nothing
        if key is None:
            raise KeyError("None can't be set!")
        #end of recursion: we found the right place for key
        if node is None: 
            #set new item._key = key and item._value= value
            return SearchTree.Node(key,value)
        #key already exists: replace old value for current
        if key == node._key:
            node._value = value
            return node
        #key must be set in left tree
        if key < node._key:
            node._left = SearchTree._tree_insert(node._left, key,value)
        #key must be set in right tree
        if key > node._key:
            node._right = SearchTree._tree_insert(node._right,key, value)
        return node
    
    @staticmethod
    #find the commuistic node of left tree 
    def _tree_predecessor (node):
        pred = node._left
        while pred._right is not None:
            pred = pred._right
        return pred 
    

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
       #key is nothing
        if key is None:
            raise KeyError("key is not set in this tree")
        if key < node._key:
            #key must be in left tree
            node._left = SearchTree._tree_remove(node._left, key)
        if key > node._key:
            #key must be in right tree
            node._right = SearchTree._tree_remove(node._right, key)
        else: 
            #now key must be node._key
            if node._left is None and node._right is None:
                #Node is a leaf node (Blatt)
                node._value = None
                node._key = None
            #Node has one child:
            elif node._left is None: 
            #set lower tree for node
                node  = node._right
            elif node._right is None:
                node = node._left
            #node has two children:
            else:
                pred = SearchTree._tree_predecessor(node)
                node._key = pred._key
                node._key = pred._value
                #remove the communistic node cuz capitalism is the best
                node._left = SearchTree._tree_remove(node._left, pred._key)
        return node
    
def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    assert t._root ==  None

    #setitem function
    t[0] = 'Hellö'
    assert t._size == 1
    assert t._root._key == 0
    t[0] = 'Hi'
    assert t._size == 1

    t[-1] = 'Hallö'
    assert t._root._left._key == -1
    assert t._size == 2
    
    #getitem functin
    value = t[0]
    assert value == 'Hi'

    #delitem function
    del t[-1]
    assert t._size == 1
    #key is not in tree
    with pytest.raises(Exception):   
        value = t[-1]


#(c) ich würde zuerst die Schlüssel sortieren. Dann wähle den mittleren key als wurzel. Teile ausgehend davon das array mit den keys in zwei gleiche 
#Teile und wähle wieder den mittleren key als wurzel des linken bzw. rechten Teilbaums. verfahre mit den Teilarrays genau so wie oben 
#(teile in zwei gleich große arrays und wähle mittlern key). Damit wird der Binärbaum ausgewogen aufgefüllt

