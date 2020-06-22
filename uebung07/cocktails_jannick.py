"""
 AlDa SS 20 - Uni Heidelberg
 Implementierung der cocktails.py von Jannick
 E-Mail: ak238@stud.uni-heidelberg.de
"""
import pytest
import json

FILE_COCKTAILS_INVERSE = "cocktails_inverse_jannick.json"


def all_ingredients(recipes):
    ...


def normalize_strings(s):
    # TODO use string patterns to normalize strings
    ...
    return s


def cocktails_inverse(recipes):
    inverse_recipes = dict()
    # TODO reverse recipes
    ...
    # TODO export inverse_recipes into FILE_COCKTAILS_INVERSE
    ...
    return inverse_recipes
