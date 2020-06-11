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
        #where is our next operator
        split = CalcTree._splitterm(term)
        # if split is 0, there is no operator anymore and it only can be a number
        if split == 0:
            return CalcTree.Number(int(term))
        
        #split into left and right operands
        leftOperand = term[:split]
        rightOperand = term[split+1:]

        # create operator node
        operatorNode = CalcTree.Operator(term[split])

        # we need to check if we enter a whole bracket term; then we slice
        if leftOperand[0] == "(":
            openB = 1
            sliceL = True
            for i in range(1,len(leftOperand)):
                if  leftOperand[i] == ")":
                    openB -= 1
                    if openB == 0 and i != len(leftOperand)-1:
                        sliceL = False
                        break
                elif leftOperand[i] == "(": openB += 1
            if sliceL: leftOperand = leftOperand[1:-1]
        operatorNode._left = CalcTree._parse(leftOperand)
        
        # we need to check if we enter a whole bracket term; then we slice
        if rightOperand[0] == "(":
            openB = 1
            sliceR = True
            for i in range(1,len(rightOperand)):
                if  rightOperand[i] == ")":
                    openB -= 1
                    if openB == 0 and i != len(rightOperand)-1:
                        sliceR = False
                        break
                elif rightOperand[i] == "(": openB += 1
            if sliceR: rightOperand = rightOperand[1:-1]
        operatorNode._right = CalcTree._parse(rightOperand)
        
        print(operatorNode._operator)
        return operatorNode


    # find operator (not in brackets) and + or - before * or /
    @staticmethod
    def _splitterm(term):
        brackets = 0
        operator = 0
        for i in range(len(term)):
            if term[i] == "(":
                brackets += 1
            elif term[i] == ")":
                brackets -= 1
                # if brackets < 0 raise value error
            if brackets == 0:
                if re.match(r"\+|\-",term[i]):
                    operator = i
                    break
                elif re.match(r"\*|\/",term[i]) and not re.match(r"\+|\-",term[operator]):
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


def test_calctree():

    tree = CalcTree("3")
    assert tree.evaluate() == 3

    tree = CalcTree("3+4*4+5")
    assert tree.evaluate() == 24

    tree = CalcTree("2*3*4+5")
    assert tree.evaluate() == 29

    tree = CalcTree("2*4*(3+(4-7)*8)-(1-6)")
    assert tree.evaluate() == 2*4*(3+(4-7)*8)-(1-6)