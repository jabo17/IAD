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
def available_cocktails(inverse_recipes, available_ingredients):
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

#(d)
def optimal_ingredients(inverse_recipes):
    #sorting the inverse_recipes by len of array
    for k in sorted(inverse_recipes, key=lambda k: len(inverse_recipes[k]), reverse=True):
        print (k)
    
    #create dict with the 15 most used ingredients
    most_used_dict = dict(inverse_recipes)
    counter = 0
    for k in inverse_recipes:
        counter += 1
        if counter >= 16:
            most_used_dict.pop(k)
    
    #create list with the 15 most needed ingredients
    most_needed_ingredients = []
    for k in most_used_dict:
        most_needed_ingredients.append(k)

    
    best_mix = []
    max_possible_cocktails = []
    #durchlaufe möglichkeiten der 15 elemente 
    for k in range(0,len(most_needed_ingredients),4):
        test_list = []
        test_list = most_needed_ingredients[k:5]
        #hier könnte man nocht die elemente k bis k+4 auslassen
        for i in range(len(most_needed_ingredients)):
            #create the test combination
            test_list.append(most_needed_ingredients[i])
            #get the list of possible cocktails
            possible_cocktails = available_cocktails(inverse_recipes, test_list)
            #now check if its the maximum
            if len(max_possible_cocktails) < len(possible_cocktails):
                max_possible_cocktails = possible_cocktails
                best_mix = test_list
            if most_needed_ingredients[i] in test_list:
                test_list.remove(most_needed_ingredients[i])
    print(max_possible_cocktails)
    return best_mix








def ignore_list(list):
    for i in list:
        if i == 'wasser':
            list.remove(i)
        elif i == 'brot':
            list.remove(i)
        elif i == 'cocktailkirschen':
            list.remove(i)
        elif i == 'pfeffer':
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
    available_recipes = available_cocktails(inverse_recipes, available_ingredients)
    print(available_recipes)

def test_optimal_ingredients():
    recipes = create_recipes()
    inverse_recipes = cocktails_inverse(recipes)
    best_mix = optimal_ingredients(inverse_recipes)
    print(best_mix)
    
def create_recipes():
    filename = 'cocktails.json'
    with open(filename) as json_file:
        recipes = json.load(json_file)
    return recipes
    



