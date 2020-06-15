#
# treap implementation by Jannick
# email: ak236@stud.uni-heidelberg.de
#

from searchtreeclass import SearchTree

#template for treap implementations
class TreapBase(SearchTree):

    class Node(SearchTree.Node):
        def __init__(self, key, value, priority):
            self._key = key
            self._priority = priority
            self._value = value
            self._left = self._right = None

    def _tree_insert():
        ...

    @staticmethod
    def _tree_rotate_left(old_root):
        ...
    
    @staticmethod
    def _tree_rotate_right(old_root):
        ...

# Wenn man Zufallszahlen verwendet, entsteht ein näherungsweise balancierter Baum.
class RandomTreap(TreapBase):
    ...

# Wenn man bei jedem Zugriff auf ein Element dessen Priorität inkrementiert (und den Baum
# umstrukturiert, falls Bedingung (2) nicht mehr erfüllt ist), entsteht ein dynamischer Baum
class DynamicTreap(TreapBase):
    ...

############## PyTest ##############

def test_random_treap():
    ...

def test_dynamic_treap():
    ...