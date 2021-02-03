#!/usr/bin/env python3

import pymysql
from VariableByteEncoder import *

class Database:
    database = None
    cursor   = None
    
    def __init__(self, databaseName, append = False):
        self.database = pymysql.connect("localhost", "root", "", databaseName)
        self.cursor   = self.database.cursor()
        if not append:
            self.CreateIngredientIndexTable()
            self.CreateRecipeInfoTable()
    
    def __del__(self):
        self.database.close()
    
    def CreateIngredientIndexTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS ingredient_index")
        self.cursor.execute("""CREATE TABLE ingredient_index (
                               ingredient             VARCHAR(255),
                               recipe_ids             BLOB,
                               ingredient_synonyms    VARCHAR(1000),
                               ingredient_temperature VARCHAR(1000))""")
    
    # def CreateIngredientIndexTable(self):
    #     self.cursor.execute("DROP TABLE IF EXISTS ingredient_index")
    #     self.cursor.execute("""CREATE TABLE ingredient_index (
    #                            ingredient             VARCHAR(255),
    #                            recipe_ids             VARCHAR(10000),
    #                            ingredient_synonyms    VARCHAR(255),
    #                            ingredient_temperature VARCHAR(255))""")
    
    def CreateRecipeInfoTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS recipe_info")
        self.cursor.execute("""CREATE TABLE recipe_info (
                               recipe_id        MEDIUMINT UNSIGNED,    
                               recipe_url       VARCHAR(1000),    
                               image_url        VARCHAR(1000),    
                               title            VARCHAR(1000),    
                               description      VARCHAR(10000),    
                               preparation_time MEDIUMINT UNSIGNED,            
                               cook_time        MEDIUMINT UNSIGNED,            
                               serving_count    MEDIUMINT UNSIGNED,
                               ingredient_count TINYINT UNSIGNED)""")
    
    def AddToIngredientIndexTable(self, ingredient, recipeId):
        recipeIds = []
        
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # If it is a new ingredient.
            recipeIds.append(recipeId)
            self.cursor.execute("INSERT INTO ingredient_index\
                                 (ingredient, recipe_ids)    \
                                 VALUES (%s, %s)", (ingredient, encode(recipeIds)))
                                 
        else:
            self.cursor.execute("SELECT recipe_ids    \
                                 FROM ingredient_index\
                                 WHERE ingredient = %s", ingredient)
            recipeIds = decode(self.cursor.fetchone()[0])
            recipeIds.append(recipeId)
            self.cursor.execute("UPDATE ingredient_index\
                                 SET recipe_ids = %s    \
                                 WHERE ingredient = %s", (encode(recipeIds), ingredient))
        
        self.database.commit()
    
    # def AddToIngredientIndexTable(self, ingredient, recipeId):    
    #     self.cursor.execute("SELECT count(*)      \
    #                          FROM ingredient_index\
    #                          WHERE ingredient = %s", ingredient)
    # 
    #     if self.cursor.fetchone()[0] == 0:    # If it is a new ingredient.    
    #         recipeIdsString = ','.join(recipeIds)
    #         self.cursor.execute("INSERT INTO ingredient_index\
    #                              (ingredient, recipe_ids)    \
    #                              VALUES (%s, %s)", (ingredient, str(recipeId)))
    #     else:
    #         self.cursor.execute("SELECT recipe_ids    \
    #                              FROM ingredient_index\
    #                              WHERE ingredient = %s", ingredient)
    #         recipeIds = self.cursor.fetchone()[0]
    #         recipeIds = recipesIds + "," + str(recipeId)
    #         self.cursor.execute("UPDATE ingredient_index\
    #                              SET recipe_ids = %s    \
    #                              WHERE ingredient = %s", (recipeIds, ingredient))
    # 
    #     self.database.commit()
    
    def AddIngredientSynonymsToIngredientIndexTable(self, ingredient, ingredientSynonyms):
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            
        else:                 
            self.cursor.execute("UPDATE ingredient_index\
                                 SET ingredient_synonyms = %s    \
                                 WHERE ingredient = %s", (ingredientSynonyms, ingredient))         
            self.database.commit()
    
    def GetIngredientSynonyms(self, ingredient):
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            return None
            
        else:
            self.cursor.execute("SELECT ingredient_synonyms\
                                 FROM ingredient_index     \
                                 WHERE ingredient = %s", ingredient)
            return self.cursor.fetchone()[0]
    
    def AddIngredientTemperatureToIngredientIndexTable(self, ingredient, ingredientTemperature):
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            
        else:
            self.cursor.execute("UPDATE ingredient_index\
                                 SET ingredient_temperature = %s    \
                                 WHERE ingredient = %s", (ingredientTemperature, ingredient))  
            self.database.commit()
    
    def GetIngredientTemperature(self, ingredient): 
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            return None
            
        else:
            self.cursor.execute("SELECT ingredient_temperature\
                                 FROM ingredient_index        \
                                 WHERE ingredient = %s", ingredient)
            return self.cursor.fetchone()[0]
    
    def AddToRecipeInfoTable(self, recipeId, recipeUrl, imageUrl, title, description,
                             preparationTime, cookTime, servingCount, ingredientCount):
        self.cursor.execute("""INSERT INTO recipe_info
                               (recipe_id, recipe_url, image_url, title, description,
                                preparation_time, cook_time, serving_count, ingredient_count)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                      (recipeId, recipeUrl, imageUrl, title, description,
                                       preparationTime, cookTime, servingCount, ingredientCount))
        self.database.commit()
    
    def GetRecipeIds(self, ingredient):
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            return []
            
        else:
            self.cursor.execute("SELECT recipe_ids    \
                                 FROM ingredient_index\
                                 WHERE ingredient = %s", ingredient)
            return decode(self.cursor.fetchone()[0])
            # return self.cursor.fetchone()[0]
    
    def GetExtendedRecipeIds(self, ingredient):
        self.cursor.execute("SELECT count(*)      \
                             FROM ingredient_index\
                             WHERE ingredient = %s", ingredient)
        
        if self.cursor.fetchone()[0] == 0:    # Cannot find the ingredient.
            print("ERROR: Cannot find %s." % ingredient)
            return []
        
        ingredientSynonyms = self.GetIngredientSynonyms(ingredient)
        recipeIds          = self.GetRecipeIds(ingredient)
        
        if ingredientSynonyms == None:
            return recipeIds
            
        else:
            ingredientSynonyms = ingredientSynonyms.split(",")
            for ingredientSynonym in ingredientSynonyms:
                recipeIds = recipeIds + self.GetRecipeIds(ingredientSynonym)
            recipeIds = list(set(recipeIds))    # Remove repeating recipe IDs.
            return recipeIds
