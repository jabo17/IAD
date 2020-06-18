from searchtreeclass import SearchTree
import random
import pytest
 

class TreapBase(SearchTree):

    class Node(SearchTree.Node):
        def __init__(self, key, value,priority):
            '''creates Node with key, value and priotity'''
            super().__init__(key,value)
            self._priority= priority
    
    def __init__(self,flag):
        '''
            possible flags are 'is_dynamic_treap', 'is_random_treap'
        '''
        super().__init__()
        self._flag = flag

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        node =TreapBase._tree_find(self._root, key)
        if node is None:
            self._size += 1
        self._root =TreapBase._tree_insert(self._root, key, value, self._flag)

    @staticmethod
    def _tree_insert(node, key, value, flag):
        if node is None:
            if flag == 'is_dynamic_treap':
                new_priority = 0
            elif flag == 'is_random_treap':
                new_priority = random.random()
            else:
                raise ValueError("flag must be dynamic or random")
            return TreapBase.Node(key, value, new_priority) 
        if node._key == key:
            node._value = value
            if flag == 'is_dymanic_treap':
                node._priority+=1
            return node
        elif key < node._key:
            node._left = TreapBase._tree_insert(node._left, key, value, flag)
            if node._left._priority > node._priority:
                node =TreapBase._tree_rotate_right(node)
        else:
            node._right = TreapBase._tree_insert(node._right, key, value, flag)
            if node._right._priority > node._priority:
                node =TreapBase._tree_rotate_left(node)
        return node
        
    
    #Rotation
    @staticmethod
    def _tree_rotate_right(old_root):
        new_root = old_root._left
        old_root.left = new_root._right
        new_root.right = old_root
        return new_root
    
    @staticmethod
    def _tree_rotate_left(old_root):
        new_root = old_root._right
        old_root._right = new_root._left
        new_root._left = old_root
        return new_root
    
    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        if node is None:
            return None
        if key < node._key:
            node._left =TreapBase._tree_remove(node._left, key)
        elif key > node._key:
            node._right = TreapBase._tree_remove(node._right, key)
        else:
            #we only need to check the priority condition if the element had two kids
            if node._left is None and node._right is None:
                node = None
            elif node._left is None:
                node = node._right
            elif node._right is None:
                node = node._left
            else:
                pred =SearchTree._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._priority = pred._priority
                node._left =TreapBase._tree_remove(node._left, pred._key)
                node = TreapBase.check_priority(node)       
        return node
    
    @staticmethod
    def check_priority(node):
        if node._left is not None and node._right is not None:
            if node._left._priority >= node._right._priority:
                if node._left._priority > node._priority:
                    #right rotate
                    node =TreapBase._tree_rotate_right(node)
                    #now: wring priority is in right tree, so check this
                    node._right =TreapBase.check_priority(node._right)
            else:
                if node._priority < node._right._priority:
                    #left rotate
                    node = TreapBase._tree_rotate_left(node)
                    #now: wrong priority is in left tree, so check this
                    node._left = TreapBase.check_priority(node._left)
        elif node._left is not None and node._right is None:
            if node._priority < node._left._priority:
                node = TreapBase._tree_rotate_right(node)
                node._right = TreapBase.check_priority(node._right)
        else: #node._right is not None and node._left is None:
            if node._priority < node._right._priority:
                #rotate left
                node = TreapBase._tree_rotate_left(node)
                node._left =TreapBase.check_priority(node._left)
        return node
            

######### Random
class RandomTreap(TreapBase):
    def __init__(self):
        super().__init__("is_random_treap")

################ Dynamic
class DynamicTreap(TreapBase):
    def __init__(self):
        super().__init__("is_dynamic_treap")
    
    @staticmethod
    def _tree_find(node, key):
        '''
            increments priority of element if existing, 
            then rebuild treap
        '''
        if node is None:
            return None
        if node._key == key:
            node._priority +=1
            return node
        if key < node._key:
            found_element = SearchTree._tree_find(node._left, key)
            if found_element is not None:
                node._left = TreapBase.check_priority(node._left)
            return found_element
        else:
            found_element = SearchTree._tree_find(node._right, key)
            if found_element is not None:
                node._right = TreapBase.check_priority(node._right)
            return found_element
    
    def top(self,min_priority):
        list =[]
        DynamicTreap._top(self._root, min_priority, list)
        return list
    
    @staticmethod
    def _top(node,min_priority, list):
        if node._priority >= min_priority:
            list.append((node._key,node._priority))
            list = DynamicTreap._top(node._left, min_priority, list)
            list = DynamicTreap._top(node._right, min_priority, list)
            return list
        else:
            return list
    

def test_random_treap():
    t = RandomTreap()
    assert len(t) == 0
    
    t[0] = "A"
    assert t.depth() == 1
    assert t._root._key == 0
    t[1] = "B"

    #grey box for keys (rotation changes place of keys)
    if t._root._right is None:
        #intern rotation
        assert t._root._left._key == 0
    else: 
        assert t._root._right._key == 1
    
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
        
    t = SearchTree()
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
    #grey box for priority
    a=t._root
    while a is not None:
        if a._right is None and a._left is None:
            a = None
        elif a._right is None:
            assert a._priority > a._left._priority
            a = t._root._left
        else:
            assert a._priority > a._right._priority 
            a = t._root._right  

#aufgabe (g)
def test_cleaned_treap():
    filename = "casanova-erinnerungen-band-2.txt"
    filestopwords = "stopwords.txt"
    w = open(filestopwords, encoding= "latin-1").read()
    s = open(filename, encoding="latin-1").read()
    for k in ',;.:-"\'!?':
        s= s.replace(k, '') 
        w = w.replace(k, 'k')# Sonderzeichen entfernen
    s = s.lower() # Alles klein schreiben
    stoptext = w.split()
    text = s.split() #string in Array von Wörtern umwandeln
    cleaned_treap = DynamicTreap()
    for word in text:
        if word in stoptext:
            text.remove(word)
    for word in text:
        cleaned_treap[word] = None

##aufgabe (e)
def compare_trees(tree1,tree2):
    if tree1._root is None and tree2._root is None:
        return True
    elif tree1._root._key == tree2._root._key: #and tree1._root._value == tree2._root._value
        var_left = compare_trees(tree1._left,tree2._left)
        var_right = compare_trees(tree1._right, tree2._right)
        if var_left == True and var_right is True:
            return True
        else:
            return False
    else:
        return False
#aufgabe (f)
def tree_element_depth(node, key, numerator):           # internal implementation
        if node is None:
            return 0
        if node._key == key:
            #if "first" root._key is already the right one
            numerator +=1
            return numerator
        if key < node._key:
            numerator +=1
            return tree_element_depth(node._left, key, numerator)  #we increment the numerator if key is in tree 
        else:
            numerator +=1
            return tree_element_depth(node._right, key, numerator)

def average_depth(tree, text):
    sum = 0
    for word in text:
        word_depth = tree_element_depth(tree._root, word, 0)
        sum += word_depth
        text.remove(word)    
    n = len(tree)
    return sum/n

def average_time(tree, text):
    sum = 0
    all_words = len(text)
    for word in text:
        word_depth = tree_element_depth(tree._root, word, 0)
        N_w = 0
        for word in text:
            N_w +=1
        sum += word_depth* (N_w/all_words)
        text.remove(word)
    return sum




#main
filename = "casanova-erinnerungen-band-2.txt"
s = open(filename, encoding="latin-1").read()
for k in ',;.:-"\'!?':
    s= s.replace(k, '') # Sonderzeichen entfernen
s = s.lower() # Alles klein schreiben
text = s.split() #string in Array von Wörtern umwandeln
rt = RandomTreap()
dt = DynamicTreap()
for word in text:
    rt[word] = None # die values werden in dieser Übung nicht benötigt
    dt[word] = None # alternativ können die values als Zähler dienen

#verschiedene Wörter
diff_words =len(dt)
print("different words in text: ", diff_words)

#Tiefe eines perfekt balancierten Baumes: T  = log_2(diff_words) = log_2(86822) = (ca) 16

#Tiefe der Bäume
print("depth of RandomTreap: ", rt.depth()) #24
print("depth of DynamicTreap: ", dt.depth()) #35

#mittlere Tiefe:
print("average depth of RandomTreap: ", average_depth(rt, text))
print("average depth of DynamicTreap: ", average_depth(dt, text))

#mittlere Zugriffszeit
print("average access time of RandomTreap: ", average_time(rt,text))
print("average access time of DynamicTreap: ", average_time(dt, text))