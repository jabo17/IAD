# -*- coding: utf8 -*-
"""
 AlDa SS 20 - Uni Heidelberg
 Implementierung der cocktails.py 
"""

import pytest
import json
import re
import copy

# Constants
FILE_COCKTAILS_INVERSE = "cocktails_inverse_jannick.json"
FILE_COCKTAILS = "cocktails.json"

#set ingredients in normalized format, they need to be in all_ingredients
IGNORE_LIST = ["wasser", "pfeffer", "zucker", "eiswürfel", "crushedice", "orangensaft", "wodka"]


# Interface

def all_ingredients(recipes: dict) -> list:
    """
    Return all normalized ingredients found in recipes.

    Args:
        recipes: name->recipe dict

    Returns:
        list: all_ingredients

    """
    ingredients = list()

    for (recipe_name, recipe) in recipes.items():
        for ingredient in recipe["ingredients"]:
            ingredient = normalize_string(ingredient)
            if ingredient not in ingredients:
                ingredients.append(ingredient)

    return ingredients


def normalize_string(s: str) -> str:
    """
    Normalizes a String

    Args:
        s: string to normalize

    Returns:
        str: normalized string
    """

    # remove text in parentheses
    s = re.sub(pattern=r'[ \xA0]*\(([^)]+)\)', repl="", string=s)
    # remove none-word-chars
    s = re.sub(pattern=r'[\s\W_]', repl="", string=s)
    # to lower case
    s = s.lower()

    return s


def cocktails_inverse(recipes: dict) -> dict:
    """
    Returns a dict which links cocktail-names (value) with a matching normalized ingredient (keys)

    Args:
        recipes: indexed list of recipes

    Returns:
        dict: normalized(ingredient)->cocktail_names

    """
    inverse_recipes = dict()

    # init key-value-pairs
    for ingredient in all_ingredients(recipes):
        inverse_recipes[ingredient] = list()

    # invert list
    for (recipes_name, recipe) in recipes.items():
        for ingredient in recipe["ingredients"]:
            inverse_recipes[normalize_string(ingredient)].append(recipes_name)

    export_inverse_recipes(inverse_recipes)

    return inverse_recipes


def possible_cocktails(inverse_recipes: dict, available_ingredients: list) -> list:
    """
    Returns possible cocktails by available ingredients

    Args:
        inverse_recipes: dict ingredient->cocktail_names
        available_ingredients: list with available ingredients

    Returns:
        list: list of possible cocktails by given ingredients and IGNORE_LIST
    """
    possible_recipes = list()

    for ingredient in IGNORE_LIST:
        if ingredient not in available_ingredients:
            available_ingredients.append(ingredient)

    for ingredient in available_ingredients:
        if ingredient in inverse_recipes:
            for recipe in inverse_recipes[ingredient]:
                if recipe not in possible_recipes:
                    possible_recipes.append(recipe)
    for ingredient in inverse_recipes.keys():
        if len(possible_recipes) == 0: break
        if ingredient not in available_ingredients:
            for recipe in inverse_recipes[ingredient]:
                if recipe in possible_recipes:
                    possible_recipes.remove(recipe)

    return possible_recipes

def optimal_ingredients(recipes: dict, inverse_recipes: dict) -> list:
    """
    Returns optimal ingredients that are needed to prepare as many cocktails as possible

    Args:
        recipes: indexed list of recipes
        inverse_recipes: dict ingredient->cocktail_names

    Returns:
        list: list of optimal ingredients
    """
    if len(inverse_recipes) <= 5:
        return list(inverse_recipes.keys())  # casting KeyView to list

    inverse_recipes_optimized = copy.copy(inverse_recipes)

    for (x, v) in inverse_recipes.items():
        if x in IGNORE_LIST:  # len(v) < 50 or
            inverse_recipes_optimized.pop(x)

    ordered_ingredients = sorted(inverse_recipes_optimized, key=lambda x: len(inverse_recipes_optimized[x]),
                                 reverse=True)

    """
        DEBUG MODE
        
        print(len(ordered_ingredients))

        print(len(inverse_recipes_optimized[ordered_ingredients[0]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[1]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[2]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[3]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[4]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[5]]))
        print(len(inverse_recipes_optimized[ordered_ingredients[-1]]))
    """

    maximum = 0
    combination = []
    # Constant for recipe minimum of ingredient
    k = 2
    #Configure Iteration Limit
    limit = 2000
    limit_counter = 0
    for a in range(0, len(ordered_ingredients) - 4):
        if len(inverse_recipes_optimized[ordered_ingredients[a]]) < k ** 5:
            # print("a", a)
            break
        for b in range(a + 1, len(ordered_ingredients) - 3):
            if len(inverse_recipes_optimized[ordered_ingredients[b]]) < k ** 4:
                # print("b", b)
                break
            for c in range(b + 1, len(ordered_ingredients) - 2):
                if len(inverse_recipes_optimized[ordered_ingredients[c]]) < k ** 3:
                    # print("c", c)
                    break
                for d in range(c + 1, len(ordered_ingredients) - 1):
                    if len(inverse_recipes_optimized[ordered_ingredients[d]]) < k ** 2:
                        # print("d", d)
                        break
                    for e in range(d + 1, len(ordered_ingredients)):
                        if limit == limit_counter:
                            return [ordered_ingredients[x] for x in combination]
                        if len(inverse_recipes_optimized[ordered_ingredients[e]]) < k:
                            # print("e", e)
                            break
                        result = possible_cocktails(inverse_recipes, [ordered_ingredients[x] for x in [a, b, c, d, e]])
                        # print([a, b, c, d, e], len(result), sep=": ")
                        if len(result) > maximum:
                            maximum = len(result)
                            combination = [a, b, c, d, e]
                            # print([ordered_ingredients[x] for x in [a, b, c, d, e]], len(result), sep=": ")
                        limit_counter += 1

    return [ordered_ingredients[x] for x in combination]


# Helper functions

def import_cocktails_from_file() -> dict:
    """
    Imports cocktail recipes from a JSON-File

    Returns:
        list: recipes
    """
    recipes = dict()

    with open(FILE_COCKTAILS, 'r', encoding="utf-8") as file:
        recipes = json.load(fp=file)

    return recipes


def export_inverse_recipes(inverse_recipes: dict) -> bool:
    """
    Exports inverse_recipes into FILE_COCKTAILS_INVERSE

    Args:
        inverse_recipes: dict ingredient->cocktail_names

    Returns:
        bool: True, if inverse_recipes was written in FILE_COCKTAILS_INVERSE
    """
    with open(FILE_COCKTAILS_INVERSE, "w", encoding="utf-8") as file:
        try:
            json.dump(obj=inverse_recipes, fp=file, indent=2)
        except ValueError as e:
            return False
    return True


# PyTests

def test_normalize_string():
    assert normalize_string("sahne (flüssig)") == "sahne"
    assert normalize_string("Sahne (flüssig meister soße) (noch so eine Klammer)") == "sahne"
    assert normalize_string("Schoko-Sahne") == "schokosahne"


def test_all_ingredients():
    recipes = import_cocktails_from_file()
    assert len(recipes) > 0

    ingredients = all_ingredients(recipes)
    assert len(ingredients) > 0

    assert "sahne" in ingredients


def test_cocktails_inverse():
    recipes = import_cocktails_from_file()
    assert len(recipes) > 0

    ingredients = all_ingredients(recipes)
    assert len(ingredients) > 0

    inverse_recipes = cocktails_inverse(recipes)

    assert len(ingredients) == len(inverse_recipes)


def test_possible_ingredients():
    recipes = import_cocktails_from_file()
    assert len(recipes) > 0

    ingredients = all_ingredients(recipes)
    assert len(ingredients) > 0

    inverse_recipes = cocktails_inverse(recipes)

    assert len(ingredients) == len(inverse_recipes)

    result = possible_cocktails(inverse_recipes, [normalize_string(s) for s in
                                                  ['zitronensaft', 'ananassaft', 'sekt', 'gin', 'bluecuracao']])
    # ["Puddingpulver", "Wodka", "Ananassaft", "Orange", "Whisky,Scotch"]])

    for r in result:
        print(r)


def test_optimal_ingredients():
    recipes = import_cocktails_from_file()
    assert len(recipes) > 0

    ingredients = all_ingredients(recipes)
    assert len(ingredients) > 0

    inverse_recipes = cocktails_inverse(recipes)

    assert len(ingredients) == len(inverse_recipes)

    result = optimal_ingredients(recipes, inverse_recipes)

    for r in result:
        print(r)
