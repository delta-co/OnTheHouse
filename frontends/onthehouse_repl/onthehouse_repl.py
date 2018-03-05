# Run this file with `py -i onthehouse_repl.py` to get some variables pre-loaded.
import os
import sys

import recipedb

rdb = recipedb.RecipeDB()

def get_untagged_ingredients():
	ingredients = rdb.get_ingredients()
	for ingredient in ingredients:
		if len(ingredient.get_tags()) == 0:
			print(ingredient)
