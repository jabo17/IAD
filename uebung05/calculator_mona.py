
#leaf nodes:
class Number:
    def __init__(self,zahl):
        self._number = int (zahl)

class Operator:
    def __init__(self,symbol):
        self._symbol = symbol
        self._left = self._right = None

# #calculator trash version
# def parse(s):
#     #put string in an array
#     a = s
#     new_number= None
#     calc_tree = Operator(None)
#     for i in range(len(a)):
#         #betr. den nächsten char
#         #is char a number?
#         if str(1) <= a[i] <= str(9):
#             new_number= Number(int(a[i]))
#             #set number in tree
#             if calc_tree._left is None:
#                 calc_tree._left = new_number
#             else:
#                 calc_tree._right = new_number
#         #now it is an algebraic symbol 
#         else:
#             new_tree = Operator(a[i])
#             #punkt vor strich:
#             if a[i] is '*' or '/':
#                 calc_tree._right = new_tree
#             else: #a[i] is '+' or '-'
#                 #arithmetische operation in höherer baumebene
#                 new_tree._left = calc_tree
#                 calc_tree = new_tree

#calculator 
def parse(s):
    a=s
    if len(a) > 1:
        #we know: number and symbol
        new_number = Number(a[0])
        if (a[1] == '+') or (a[1]=='-'):
            print("lol")
            print(a[1])
            new_operator = Operator(a[1])
            new_operator._left = new_number
            new_operator._right = parse(a[2:len(a)])
            
        else:
            #now a[1] is * or /
            for i in range(len(a)):
                if (a[i] == '+') or (a[i]== '-'):
                    #call function with argument without + or -
                    #insert tree at left
                    new_operator = Operator(a[i])
                    print(a[i])
                    new_operator._left = parse(a[0:i])
                    if len(a) == i+2:
                        #only one number left
                        new_operator._right = Number(a[i+1])._number
                    print("was")
                    print(new_operator._left._symbol, new_operator._symbol,new_operator._right)
                    return new_operator
            #now string has no arithmetic expression +,-
            new_operator = Operator(a[1])
            new_operator._left = new_number
            new_operator._right = parse(a[2:len(a)])
        print("was geht")
        print(new_operator._left._number, new_operator._symbol,new_operator._right)
        return new_operator
    elif len(a)==1:
        return Number(a[0])._number
        
    else: 
        raise AssertionError ("no arithmetic expression!")

#main
a = parse('1*1+1')
print(a)

    
        


