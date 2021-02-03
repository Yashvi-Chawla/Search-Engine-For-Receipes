#!/usr/bin/env python3

import pymysql
import operator
from VariableByteEncoder import *

database = pymysql.connect("shareddb-r.hosting.stackcp.net", "tingsheng", "ts123123", "recipes-3132330cb1")
cursor   = database.cursor()

cursor.execute("SELECT ingredient, recipe_ids FROM ingredient_index")
result = cursor.fetchall()

ingredientDict = dict()
for row in result:
    key = row[0]
    value = len(decode(row[1]))
    ingredientDict.update({key: value})

sortedIngredientDict = dict(sorted(ingredientDict.items(), key=operator.itemgetter(1), reverse=True))

outputFile = open('IngredientsFromMostCommonToLeastCommon.txt', 'w')
for key in sortedIngredientDict:
    outputFile.write("%s\t\t\t%s\n" % (key, sortedIngredientDict[key]))
