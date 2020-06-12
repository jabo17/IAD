import pytest
import re

class CalcTree:
    #node classes
    class Number:
        def __init__(self, number):
            self._number = number
    class Operator:
        def __init__(self, operator):
            self._operator = operator
            self._left = self._right = None
        
    # creates a calctree by parsing a term
    def __init__(self, term):
        self._rootOperator = CalcTree._parse(term)

    def evaluate(self):
        return CalcTree._evaluate_tree(self._rootOperator)
    
    # method to parse a term into a calctree
    @staticmethod
    def _parse(term):
        if(len(term)) == 0:
            raise ValueError("Term has length null")
        #where is our next operator
        split = CalcTree._splitterm(term)
        #arithmetic expression with many brackets ((())) or at least one()
        while split == 0 and term[0] == "(":
            term = term[1:-1]
            split = CalcTree._splitterm(term)
        # if split is 0, there is no operator anymore and it only can be a number
        if split == 0:
            try:
                number = int(term)
            except ValueError:
                raise ValueError("no valid arithmetic term")
            return CalcTree.Number(number)
        
        #split into left and right operands
        leftOperand = term[:split]
        rightOperand = term[split+1:]

        # create operator node
        operatorNode = CalcTree.Operator(term[split])

        # we need to check if we enter a whole bracket term; then we slice
        operatorNode._left = CalcTree._parse(leftOperand)
        
        # we need to check if we enter a whole bracket term; then we slice
        operatorNode._right = CalcTree._parse(rightOperand)
        
        #print(operatorNode._operator)
        return operatorNode


    # find operator (not in brackets) and + or - before * or /
    @staticmethod
    def _splitterm(term):
        brackets = 0
        operator = 0
        #(3+4+5)
        for i in range(len(term)):
            if term[i] == "(":
                brackets += 1
            elif term[i] == ")":
                brackets -= 1
                # if brackets < 0 raise value error
            elif brackets == 0:
                if re.match(r"\+|\-",term[i]):
                    operator = i
                    break
                elif re.match(r"\*|\/",term[i]): #and not re.match(r"\+|\-",term[operator])
                    operator = i
        return operator

    # @param node is a operator node in a tree
    # it recursively evaluates the calctree
    @staticmethod
    def _evaluate_tree(node):
        leftOperand = 0
        rightOperand = 0

        #print(node._operator)
        if isinstance(node, CalcTree.Number):
            return node._number
        if isinstance(node._left, CalcTree.Number):
            leftOperand = node._left._number
        else:
            leftOperand = CalcTree._evaluate_tree(node._left)
        if isinstance(node._right, CalcTree.Number):
            rightOperand = node._right._number
        else:
            rightOperand = CalcTree._evaluate_tree(node._right)
        
        if node._operator == "+":
            return leftOperand + rightOperand
        elif node._operator == "-":
            return leftOperand - rightOperand
        elif node._operator == "*":
            return leftOperand * rightOperand
        else:
            return leftOperand / rightOperand

## interface von Aufgabenstellung
def parse(term):
    return CalcTree(term)

def evaluate(tree):
    return tree.evaluate()


def test_calctree():

    tree = parse("3")
    assert evaluate(tree) == 3

    tree = parse("(3)")
    assert evaluate(tree) == 3

    tree = parse("3+4*4+5")
    assert evaluate(tree) == 24

    tree = CalcTree("2*3*4+5")
    assert evaluate(tree) == 29
    
    with pytest.raises(ValueError):
        tree = CalcTree("lasdj")

    tree = parse("2*4*(3+(4-7)*8)-(1-6)")
    assert evaluate(tree) == 2*4*(3+(4-7)*8)-(1-6)

    tree = parse("(((2*4*(3+(4-7)*8)-(1-6))))")
    assert evaluate(tree) == 2*4*(3+(4-7)*8)-(1-6)