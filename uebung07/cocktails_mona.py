import json


def all_ingredients(recipes):
    list = []   
    ingredients = "ingredients"
    for cocktail in recipes:   #Name Cocktail Ebene
        for l in recipes [cocktail][ingredients]:
            normal = normalize_strings(l)
            if normal not in list:
                list.append(normal)
    return list

def normalize_strings(s):
    #alles innerhalb der klammern entfernen
    for i in range(len(s)):
        if s[i] == '(':
            for l in range(i+1,len(s)):
                if s[l] == ')' and l != len(s)-1:
                    s = s[0:i] + s[l+1: len(s)]
                    s = normalize_strings(s)
                    break
                elif s[l] == ')':
                    s = s[0:i]
                    break
                #falls jemand klammern auf und vergessen zu zumachen
                elif l == len(s)-1:
                    s = s[0:i]
            break
    #Grossbuchstaben entfernen
    s = s.lower()
    #falls sich unnötige Sonderzeichen eingeschlichen haben:
    for k in ',;.:-"\'!?':
        s = s.replace(k, '')
    return s

#(b)
def cocktails_inverse(recipes):
    new_dict = dict() 
    ingredients = "ingredients"
    for cocktail in recipes:   #Name Cocktail Ebene
        for l in recipes [cocktail][ingredients]:
            normal = normalize_strings(l)
            if normal not in new_dict:
                new_dict.update({normal: []})
            new_dict[normal].append(cocktail)
    return new_dict

#(c)
def possible_cocktails(inverse_recipes, available_ingredients):
    #normalize the strings
    for i in range(len(available_ingredients)):
        available_ingredients[i] = normalize_strings(available_ingredients[i])
    #remove unnecessary elements 
    available_ingredients = ignore_list(available_ingredients)
    
    #create list, with not possible recipes and possible recipes
    not_available_recipes = []
    available_recipes = []
    for k in inverse_recipes:
        if k in available_ingredients:
            #fuege alle rezepte hinzu, die noch nicht enthalten waren
            for i in inverse_recipes[k]:
                if i not in available_recipes:
                    available_recipes.append(i)
        else:
            for i in inverse_recipes[k]:
                if i not in not_available_recipes:
                    not_available_recipes.append(i)
    
    #now remove the recipes that are not possible
    for k in not_available_recipes:
        if k in available_recipes:
            available_recipes.remove(k)

    return available_recipes

def ignore_list(list):
    for i in list:
        if i == 'wasser':
            list.remove(i)
        elif i == 'brot':
            list.remove(i)
        elif i == 'cocktailkirschen':
            list.remove(i)
    return list
                    

def test_normalize_strings():
    a = 'Sahne(30%)(flüssig)(le'
    a = normalize_strings(a)
    assert a == 'sahne'

def test_all_ingredients():
    recipes = create_recipes()

    list = all_ingredients(recipes)
    for i in range(len(list)):
        for k in range(i+1, len(list)):
            if list[i]==list[k]:
                raise Exception

# def test_cocktails_inverse():
#     recipes = create_recipes()

#     new_dict = cocktails_inverse(recipes)
#     #sorting the dict by length of the cocktail lists
#     for k in sorted(new_dict, key=lambda k: len(new_dict[k]), reverse=True):
#         print (k)
#     #print(new_dict)

#     #create list with most needed ingredients
#     most_needed = []
#     for i in new_dict:
#         if len(most_needed) == 15:
#             break
#         most_needed.append(i)
    #print(most_needed)

def test_possible_cocktails():
    recipes = create_recipes()
    inverse_recipes = cocktails_inverse(recipes)
    available_ingredients = ['maracujasaft', 'crushed ice', 'maracujasirup', 'orangensaft', 'kokossirup', 'sahne', 'blue curacao', 'meersalz ', 'wodka']
    available_recipes = possible_cocktails(inverse_recipes, available_ingredients)
    print(available_recipes)
    
def create_recipes():
    filename = 'cocktails.json'
    with open(filename) as json_file:
        recipes = json.load(json_file)
    return recipes
    



