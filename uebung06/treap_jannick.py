#
# treap implementation by Jannick
# email: ak236@stud.uni-heidelberg.de
#

from searchtreeclass import SearchTree, test_search_tree
import pytest
import random

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
            self._key = key
            self._priority = priority
            self._value = value
            self._left = self._right = None
    
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
def compare_trees(tree1, tree2):
    ...

############## PyTest ##############

def test_random_treap():
    ##whitebox test: test_search_tree
    ##gray box test:
    ...

def test_dynamic_treap():
    ##whitebox test: test_search_tree
    ##gray box test:
    
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

def test_word_dic(texts):
    print("treap dics")
    for text in texts:
        dt = DynamicTreap()
        rt = RandomTreap()
        for w in text:
            dt[w] = None
            rt[w] = None
        print(dt.top(100)[0:100])
        print(dt.depth())
        print(len(dt))
        print(rt.depth())
        print(len(rt))

## aufgabe g)
def test_cleaned_word_dic(texts):
    print("cleaned treap dics")
    stopwords = open("stopwords.txt", encoding="latin-1").read()
    stopwords = stopwords.split()
    # rather than a set, we use our one dynamic tree
    stopword_tree = DynamicTreap()
    for w in stopwords:
        stopword_tree[w] = True
    for text in texts:
        dt = DynamicTreap()
        rt = RandomTreap()
        for w in text:
            try:
                stopword_tree[w]
            except KeyError:
                dt[w] = None
                rt[w] = None
        print(dt.top(20)[0:100])
        print(dt.depth())
        print(len(dt))
        print(rt.depth())
        print(len(rt))

## aufgabe f)