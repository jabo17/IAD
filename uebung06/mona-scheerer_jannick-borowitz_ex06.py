#
# treap implementation by Mona, Jannick
#
# test_texts should be allocated in same dictionary
#

from korrektur_searchtree import SearchTree
import pytest
import random
import numpy
#template for treap implementations
class TreapBase(SearchTree):

    class Node(SearchTree.Node):
        def __init__(self, key, value, priority):
            """
                Constructs a BaseTreap.Node based on a SearchTree.Node.
                
                Parameters:
                    key
                    value
                    priority
            """
            super().__init__(key, value)
            self._priority = priority
    
    def __init__(self, flag):
        """
            Constructs a BaseTreap based on a SearchTree
            for a given flag.

            Possible flags are: is_dynamic_treap, is_random_treap
        """
        super().__init__()
        self._flag = flag

    #Ist der key noch nicht im Treap enthalten, wird er nach der Such-
    # baumregel eingefügt und der Baum nach den Prioritäten umstrukturiert, wenn erforderlich
    # Ist der key bereits vorhanden, wird beim RandomTreap nur der value ersetzt (die Priorität bleibt
    # unverändert), während beim DynamicTreap zusätzlich die Priorität um Eins erhöht und der
    # Baum gegebenenfalls umstrukturiert wird.
    def __setitem__(self, key, value):
        """
            Removes a node from the tree by a given key.
        """
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            self._size += 1
        # call _tree_insert and pass flag
        self._root = TreapBase._tree_insert(self._root, key, value, self._flag)

    def __delitem__(self, key):
        """
            Removes a node from the tree by a given key and the initialised flag-mode.

            If the key was not found, a ValueError for key is raised.
        """
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError("key not found")
        self._size -= 1
        self._root = TreapBase._tree_remove(self._root, key)


    @staticmethod
    def _tree_insert(node, key, value, flag):
        """
            Inserts a value key-specific into the given node-hierarchy

            There are two supported modes:
                flag="is_dynamic_treap"
                flag="is_random_treap"
            Otherwise a ValueError for flag is raised.
            
            It fulfills the binary-searchtree and heap conditions.
        """
        if node is None:
            priority = 0
            if flag == "is_random_treap":
                priority = random.randint(0,10**32) 
            elif flag == "is_dynamic_treap":
                priority = 0
            else:
                raise ValueError("flag must be 'is_dynamic_treap' oder 'is_random_treap'")
            return TreapBase.Node(key, value, priority)
        if node._key == key:
            node._value = value
            if flag == "is_dynamic_treap":
                node._priority += 1
            return node
        elif key < node._key:
            node._left = TreapBase._tree_insert(node._left, key, value, flag)
            if node._priority < node._left._priority:
                return TreapBase._tree_rotate_right(node)
        else:
            node._right = TreapBase._tree_insert(node._right, key, value, flag)
            if node._priority < node._right._priority:
                return TreapBase._tree_rotate_left(node)
        return node

    # it is almost the same as searchtree's _tree_remove, but case 3
    # has changed: swap priority + fulfil heap condition
    @staticmethod
    def _tree_remove(node, key):
        """
            Removes a node by a key in the given node-hierarchy.
            
            It fulfills the binary-searchtree and heap condition.
        """
        if node is None:
            return None
        if key < node._key:
            node._left = TreapBase._tree_remove(node._left, key)
        elif key > node._key:
            node._right = TreapBase._tree_remove(node._right, key)
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
                node._priority = pred._priority
                node._left = SearchTree._tree_remove(node._left, pred._key)

                #heap condition could no longer be met
                node = TreapBase._tree_heapify(node)
        return node

    # aufgabe a
    @staticmethod
    def _tree_rotate_left(old_root):
        new_root = old_root._right
        old_root._right = new_root._left
        new_root._left = old_root
        return new_root
    
    @staticmethod
    def _tree_rotate_right(old_root):
        new_root = old_root._left
        old_root._left = new_root._right
        new_root._right = old_root
        return new_root

    # it is not the typical heapify function
    # rather than swapping we need to rotate nodes
    # this is because, we are not allowed to break the search tree condition
    # the result is a priority based balanced tree fulfilling the heap condition regarding the priority of nodes
    @staticmethod
    def _tree_heapify(node):
        if node._left != None and node._right != None:
            if node._left._priority >= node._right._priority:
                if node._left._priority > node._priority:
                    # right rotate
                    node = TreapBase._tree_rotate_right(node)
                    node._right = TreapBase._tree_heapify(node._right)
            else:
                if node._right._priority > node._priority:
                    # left rotate
                    node = TreapBase._tree_rotate_left(node)
                    node._left = TreapBase._tree_heapify(node._left)
        elif node._left != None and node._left._priority > node._priority:
            # right rotate
            node = TreapBase._tree_rotate_right(node)
            node._right = TreapBase._tree_heapify(node._right)
        elif node._right != None and node._right._priority > node._priority:
            # left rotate
            node = TreapBase._tree_rotate_left(node)
            node._left = TreapBase._tree_heapify(node._left)
        return node

# Wenn man Zufallszahlen verwendet, entsteht ein näherungsweise balancierter Baum.
class RandomTreap(TreapBase):
    def __init__(self):
        super().__init__("is_random_treap")

# Wenn man bei jedem Zugriff auf ein Element dessen Priorität inkrementiert (und den Baum
# umstrukturiert, falls Bedingung (2) nicht mehr erfüllt ist), entsteht ein dynamischer Baum
class DynamicTreap(TreapBase):
    def __init__(self):
        """
            Intializes a DynamicTreap

            Therefore the parent is constructed with flag="is_dynamic_treap"
        """
        super().__init__("is_dynamic_treap")

    def __getitem__(self, key):
        """
            Search for a key in the DynamicTreap.
        """
        node = DynamicTreap._tree_find(self._root, key)
        if node is None:
            raise KeyError("key not found")
        # heap condition for root could not longer be met
        self._root = TreapBase._tree_heapify(self._root)
        return node._value

    @staticmethod
    def _tree_find(node, key):
        """ 
            Finds a node in DynamicTreap.
            
            In the case of a match it increments the priority by 1 of the node
            and heapifies the tree accordingly.
        """
        if node is None:
            return None
        if node._key == key:
            node._priority += 1
            return node
        if key < node._key:
            match = DynamicTreap._tree_find(node._left, key)
            if match is not None:
                # heapifies left tree (max recursion depth: 2)
                node._left = TreapBase._tree_heapify(node._left)
            return match
        else:
            match = DynamicTreap._tree_find(node._right, key)
            if match is not None:
                # heapifies left tree (max recursion depth: 2)
                node._right = DynamicTreap._tree_heapify(node._right)
            return match         
    
    def top(self, min_priority):
        """ 
            Returns an array of key-priority-tuples of nodes
            with a min priority
        """
        list = []
        DynamicTreap._tree_top(self._root, min_priority, list)
        return list

    @staticmethod
    def _tree_top(node, min_priority, list):
        """
            Adds a node and its childs as key-priority-tuples to a list 
            with a min priority.
        """
        if node is not None and node._priority >= min_priority:
            list.append((node._key, node._priority))
            DynamicTreap._tree_top(node._left, min_priority, list)
            DynamicTreap._tree_top(node._right, min_priority, list)

## aufgabe e
## return true, if both trees are equally sorted and have equal elements
def compare_trees(tree1,tree2):
    return compare_nodes(tree1._root, tree2._root)
    

def compare_nodes(node1,node2):
    if node1 is None and node2 is None:
        return True
    elif node1._key == node2._key: #and node1._value == node2._value
        return compare_nodes(node1._left,node2._left) and compare_nodes(node1._right, node2._right)
    else:
        return False

############ aufgabe f) ####################
def average_depth(tree):
    pairs = key_value_depths(tree)
    sum_depth = 0
    for (matches, depth) in pairs:
        sum_depth += depth
    n = len(tree)
    return sum_depth/n

def average_access_time(tree, N): # N = len(text)
    pairs = key_value_depths(tree)
    sum = 0
    for (matches, depth) in pairs:
        sum += (matches/N) * depth
    n = len(tree)
    return sum/n   

def _key_value_depth(node,pairs, depth):
    """
        get all (key, value, depth)pairss of a node
    """
    if node is not None:
        pairs.append((node._value, depth+1))
        _key_value_depth(node._left,pairs, depth+1)
        _key_value_depth(node._right,pairs, depth+1)

def key_value_depths(tree):
    """
        get all (key, value, depth)pairss of a tree
    """
    pairs = []
    _key_value_depth(tree._root,pairs, -1)
    return pairs

############## Unit PyTests ##############

def check_treap(getTreapInstance):

    t = getTreapInstance()
    assert len(t) == 0
    
    t[1] = 1
    assert len(t) == 1
    assert t[1] == 1
    with pytest.raises(KeyError):
        v = t[2]
    
    t[0] = 0
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 1
    
    t[1] = 11                # overwrite value of existing key
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    
    t[2] = 2
    assert len(t) == 3
    assert t[0] == 0
    assert t[1] == 11
    assert t[2] == 2
    
    del t[2]                 # delete leaf
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    with pytest.raises(KeyError):
        v = t[2]
        
    del t[1]                 # replace node with left child
    assert len(t) == 1
    assert t[0] == 0
    with pytest.raises(KeyError):
        v = t[1]

    with pytest.raises(KeyError):
        del t[1]             # delete invalid key
        
    t = getTreapInstance()
    t[0]=0
    t[3]=3
    t[1]=1
    t[2]=2
    t[4]=4
    assert len(t) == 5
    for k in [0, 1, 2, 3, 4]:
        assert t[k] == k
        
    del t[3]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[3]
    assert len(t) == 4
    for k in [0, 1, 2, 4]:
        assert t[k] == k
        
    del t[2]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[2]
    assert len(t) == 3
    for k in [0, 1, 4]:
        assert t[k] == k
        
    del t[1]                 # replace node with right child
    with pytest.raises(KeyError):
        v = t[1]
    assert len(t) == 2
    for k in [0, 4]:
        assert t[k] == k
        
    del t[4]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[4]
    assert len(t) == 1
    assert t[0] == 0
        
    del t[0]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[0]
    assert len(t) == 0

    t[-1] = "C"

    # test random access
    # depending on the tree priorities change
    # we check the priorities later
    for i in range(20):
        with pytest.raises(KeyError):
            t[random.randint(0, 5)]

    #grey box for priority (heap condition)
    check_priority(t._root)
    #grey box for search tree condition
    check_bin_tree_cond(t._root)

def check_priority(a):
    """
        verifies heap condition for (sub) tree 
    """
    if a is None:
        return True
    elif a._right is None and a._left is None:
        a = None
        check_priority(a)
    elif a._right is None:
        assert a._priority > a._left._priority
        return check_priority(a._left)
    elif a._left is None:
        assert a._priority > a._right._priority
        return check_priority(a._right)
    else:
        assert a._priority > a._right._priority and a._priority > a._left._priority
        return check_priority(a._right) and check_priority(a._left) 

def check_bin_tree_cond(a):
    """
        verifies binary search tree condition for (sub) tree
    """
    if a is None:
        return True
    if a._left is not None:
        assert a._left._key < a._key
    if a._right is not None:
        assert a._right._key > a._key
    return check_bin_tree_cond(a._left) and check_bin_tree_cond(a._right)

def test_dynamic_treap():

    check_treap(lambda: DynamicTreap())    


    # test dynamicTreap (especially for top())
    tree = DynamicTreap()
    tree[5] = 5
    tree[2] = 2
    tree[8] = 8
    tree[1] = 1
    tree[3] = 3

    assert tree._root._key == 5
    assert tree._root._priority == 0

    assert tree[3] == 3
    assert tree[2] == 2
    assert tree[2] == 2

    assert tree._root._key == 2
    assert tree._root._priority == 2
    assert tree._root._right._key == 3

    del tree[2]

    assert tree._root._key == 3
    assert tree._root._priority == 1

    assert tree._root._left._key == 1

    assert tree[8] == 8

    top = tree.top(1)
    assert len(top) == 2
    assert (8,1) in top
    assert (3,1) in top

def test_random_treap():
    check_treap(lambda: RandomTreap())  

# print comparison
def print_compare_trees(dt, rt, text):
    # wir geben die 100 ersten woerter von top aus
    print("Max 100 Woerter mit groesster Prioritaet, ermittelt mittels dt.top(20): ")
    print(sorted(dt.top(20), reverse= True , key= lambda x: x[1])[0:100])
    print("Anzahl (unterschiedlicher) Woerter in DT: ", len(dt))
    print("Anzahl (unterschiedlicher) Woerter in RT: ", len(rt))
    assert len(dt) == len(rt)
    print("Tiefe eines perfekt balancierten Baumes: ", numpy.log2(len(dt)))
    print("Tiefe von DT: ", dt.depth())
    print("Tiefe von RT: ", rt.depth())

    #aufgabe f
    N= len(text)
    print("Avg. Depth of RT: ", average_depth(rt))
    print("Avg. Depth or DT: ", average_depth(dt))
    #anhand der Ausgabe sehen wir: average_depth(rt) < average_depth(dt)
    print("Avg. Access Time of RT: ", average_access_time(rt, N))
    print("Avg. Access Time of DT: ", average_access_time(dt, N))

#aufgabe d)
@pytest.fixture
def text_list():
    return [
        "casanova-erinnerungen-band-2.txt",
        "die-drei-musketiere.txt",
        "helmholtz-naturwissenschaften.txt"
    ]

@pytest.fixture
def texts(text_list):
    texts = []
    for filename in text_list:
        s = open(filename, encoding="latin-1").read()
        for k in ',;.:-"\'!?':
            s = s.replace(k, '')
        s = s.lower()
        text = s.split()
        texts.append(text)
    return texts

#to get output: use -s with pytest
def test_word_dic(texts, text_list):
    print("treap dics")
    for i in range(len(texts)):
        text = texts[i]
        print("######## ", text_list[i], " ########")
        dt = DynamicTreap()
        rt = RandomTreap()
        for w in text:
            try:
                found = rt[w]
            except:
                found = 0
            # the value is a counter apperances in the tree
            dt[w] = found + 1
            rt[w] = found + 1
        print_compare_trees(dt, rt, text)

## aufgabe g)
def test_cleaned_word_dic(texts, text_list):
    print("cleaned treap dics")
    stopwords = open("stopwords.txt", encoding="latin-1").read()
    stopwords = stopwords.split()
    # rather than a set, we use our one dynamic treap
    stopword_tree = DynamicTreap()
    for w in stopwords:
        stopword_tree[w] = True
    for i in range(len(texts)):
        text = texts[i]
        print("######## ", text_list[i], " ########")
        dt = DynamicTreap()
        rt = RandomTreap()
        for w in text:                
            try:
                #try to increment priority in stopword_tree of key w
                stopword_tree[w]
            except KeyError:
                # w is not in stopword_tree
                try:
                    found = rt[w]
                except:
                    found = 0
                # the value is a counter apperances in the tree
                dt[w] = found + 1
                rt[w] = found + 1
        print("####### Cleaned Text #######")
        print_compare_trees(dt, rt, text)