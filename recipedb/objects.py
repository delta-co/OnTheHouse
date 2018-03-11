import bcrypt
from flask_login import UserMixin

from . import constants
from . import exceptions
from . import helpers

from voussoirkit import sqlhelpers


# Can be used in isinstance checks.
NoneType = type(None)


class ObjectBase:
    def __init__(self, recipedb):
        super().__init__()
        self.recipedb = recipedb

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and
            self.recipedb == other.recipedb and
            self.id == other.id
        )

    def __format__(self, formcode):
        if formcode == 'r':
            return repr(self)
        else:
            return str(self)

    def __hash__(self):
        return hash(self.id)


class Image(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_IMAGE_COLUMNS, db_row))

        self.id = db_row['ImageID']
        self.file_path = db_row['ImageFilePath']

    def __repr__(self):
        return 'Image:%s' % self.id


class Ingredient(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_INGREDIENT_COLUMNS, db_row))

        self.id = db_row['IngredientID']
        self.name = db_row['Name']
        self.description = db_row['Description']
        self.ingredient_image_id = db_row['IngredientImageID']

    def __repr__(self):
        return 'Ingredient:%s:%s' % (self.id, self.name)

    def add_autocorrect(self, alternate_name):
        alternate_name = self.recipedb._normalize_ingredient_name(alternate_name)
        try:
            existing = self.recipedb.get_ingredient_by_name(alternate_name)
        except exceptions.NoSuchIngredient:
            pass
        else:
            raise exceptions.IngredientExists(alternate_name)
        cur = self.recipedb.sql.cursor()

        data = {
            'IngredientID': self.id,
            'AlternateName': alternate_name,
        }
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENTAUTOCORRECT_COLUMNS, data)
        query = 'INSERT INTO IngredientAutocorrect VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def add_tag(self, tag):
        if self.has_tag(tag):
            return

        cur = self.recipedb.sql.cursor()
        data = {
            'IngredientID': self.id,
            'IngredientTagID': tag.id,
        }
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENTINGREDIENTTAG_COLUMNS, data)
        query = 'INSERT INTO Ingredient_IngredientTag_Map VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def get_tags(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT IngredientTagID FROM Ingredient_IngredientTag_Map WHERE IngredientID = ?', [self.id])
        lines = cur.fetchall()
        tags = {self.recipedb.get_ingredient_tag_by_id(line[0]) for line in lines}

        return tags

    def has_tag(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute(
            'SELECT * FROM Ingredient_IngredientTag_Map WHERE IngredientID = ? AND IngredientTagID = ?',
            [self.id, tag.id]
        )
        exists = cur.fetchone()
        return bool(exists)

    def remove_tag(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute('DELETE FROM Ingredient_IngredientTag_Map WHERE IngredientID = ? AND IngredientTagId = ?',
            [self.id, tag.id]
        )
        self.recipedb.sql.commit()

    def rename(self, name):
        # Check if `name` is already taken by an other ingredient
        # or is in the autocorrect table.
        raise NotImplementedError


class IngredientTag(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_INGREDIENTTAG_COLUMNS, db_row))

        self.id = db_row['IngredientTagID']
        self.name = db_row['TagName']
        self.parent_id = db_row['ParentTagID']

    def __repr__(self):
        return 'IngredientTag:%s:%s' % (self.id, self.name)

    def add_child(self, tag):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT ParentTagID FROM IngredientTag WHERE IngredientTagID = ?', [tag.id])
        row = cur.fetchone()[0]
        if row is not None:
            raise exceptions.AlreadyHasParent(tag=tag, parent=self)

        data = {
            'IngredientTagID': tag.id,
            'ParentTagID': self.id,
        }
        (query, bindings) = sqlhelpers.update_filler(data, where_key='IngredientTagID')
        query = 'UPDATE IngredientTag %s' % query
        cur.execute(query, bindings)
        tag.parent_id = self.id
        self.recipedb.sql.commit()

    def get_children(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM IngredientTag WHERE ParentTagID = ?', [self.id])
        rows = cur.fetchall()
        tags = set(IngredientTag(self.recipedb, row) for row in rows)
        return tags

    def get_parent(self):
        if self.parent_id is None:
            return None

        return self.recipedb.get_ingredient_tag_by_id(self.parent_id)

    def leave_parent(self):
        parent = self.get_parent()
        if parent is None:
            return

        data = {
            'ParentTagID': None,
            'IngredientTagID': self.id,
        }
        cur = self.recipedb.sql.cursor()
        (query, bindings) = sqlhelpers.update_filler(data, where_key='IngredientTagID')
        query = 'UPDATE IngredientTag %s' % query
        cur.execute(query, bindings)
        self.parent_id = None
        self.recipedb.sql.commit()

    def rename(self, name):
        # Check if `name` is already taken somewhere else.
        raise NotImplementedError


class QuantitiedIngredient(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)

        if not db_row:
            return

        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_RECIPEINGREDIENT_COLUMNS, db_row))

        self.ingredient = self.recipedb.get_ingredient(id=db_row['IngredientID'])
        self.quantity = db_row['IngredientQuantity']
        self.prefix = db_row['IngredientPrefix']
        self.suffix = db_row['IngredientSuffix']

    def __eq__(self, other):
        return isinstance(other, QuantitiedIngredient) and self._identity == other._identity

    def __hash__(self):
        return hash(self._identity)

    def __repr__(self):
        return '%s of %s' % (self.quantity, self.ingredient)

    @property
    def _identity(self):
        return (self.ingredient.id, self.quantity, self.prefix, self.suffix)

    @classmethod
    def from_existing(cls, ingredient, *, quantity=None, prefix=None, suffix=None):
        self = cls(ingredient.recipedb, db_row=None)
        self.ingredient = ingredient
        self.quantity = quantity
        self.prefix = prefix
        self.suffix = suffix
        return self


class Recipe(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_RECIPE_COLUMNS, db_row))

        self.id = db_row['RecipeID']
        self.name = db_row['Name']
        self.slug = helpers.slugify(self.name)
        self.author_id = db_row['AuthorID']
        if self.author_id is not None:
            self.author = self.recipedb.get_user(id=self.author_id)
        else:
            self.author = None
        self.country = db_row['CountryOfOrigin']
        self.meal_type = db_row['MealType']
        self.cuisine = db_row['Cuisine']
        self.prep_time = db_row['PrepTime']
        self.date_added = db_row['DateAdded']
        self.date_mod = db_row['DateModified']
        self.blurb = db_row['Blurb']
        self.serving_size = db_row['ServingSize']
        self.instructions = db_row['Instructions']
        self.recipe_image_id = db_row['RecipeImageID']

    def __repr__(self):
        return 'Recipe:%s:%s' % (self.id, self.slug)

    def edit(
            self,
            *,
            blurb=None,
            country=None,
            cuisine=None,
            ingredients=None,
            instructions=None,
            meal_type=None,
            name=None,
            prep_time=None,
            recipe_image=None,
            serving_size=None,
        ):
        if blurb is not None:
            self.blurb = blurb
        if country is not None:
            self.country = country
        if cuisine is not None:
            self.cuisine = cuisine
        if ingredients is not None:
            self.set_ingredients(ingredients)
        if instructions is not None:
            instructions = instructions.replace('\r', '')
            self.instructions = instructions
        if meal_type is not None:
            self.meal_type = meal_type
        if name is not None:
            self.name = name
            self.slug = helpers.slugify(self.name)
        if prep_time is not None:
            self.prep_time = prep_time
        if recipe_image is not None:
            self.recipe_image_id = recipe_image.id
        if serving_size is not None:
            self.serving_size = serving_size
        query = '''
        UPDATE Recipe SET
            Blurb=?,
            CountryOfOrigin=?,
            Cuisine=?,
            DateModified=?,
            Instructions=?,
            MealType=?,
            Name=?,
            PrepTime=?,
            RecipeImageID=?,
            ServingSize=?
        WHERE RecipeID=?
        '''
        bindings = [
            self.blurb,
            self.country,
            self.cuisine,
            helpers.now(),
            self.instructions,
            self.meal_type,
            self.name,
            self.prep_time,
            self.recipe_image_id,
            self.serving_size,
            self.id
        ]
        cur = self.recipedb.sql.cursor()
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def get_ingredients(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Recipe_Ingredient_Map WHERE RecipeID = ?', [self.id])
        lines = cur.fetchall()
        ingredients = {QuantitiedIngredient(self.recipedb, line) for line in lines}

        return ingredients

    def get_ingredients_and_tags(self):
        everything = {qi.ingredient for qi in self.get_ingredients()}
        tags = set()
        for ingredient in everything:
            tags.update(ingredient.get_tags())
        everything.update(tags)
        while len(tags) > 0:
            tags = {tag.get_parent() for tag in tags}
            tags = {tag for tag in tags if tag is not None}
            everything.update(tags)
        return everything

    def get_reviews(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Review WHERE RecipeID = ?', [self.id])
        rows = cur.fetchall()
        reviews = [Review(self.recipedb, row) for row in rows]
        reviews.sort(key=lambda x: x.date_added, reverse=True)
        return reviews

    def set_ingredients(self, ingredients):
        ingredients = [self.recipedb._coerce_quantitied_ingredient(i) for i in ingredients]
        cur = self.recipedb.sql.cursor()
        cur.execute('DELETE FROM Recipe_Ingredient_Map WHERE RecipeID = ?', [self.id])

        for quant_ingredient in ingredients:
            recipe_ingredient_data = {
                'RecipeID': self.id,
                'IngredientID': quant_ingredient.ingredient.id,
                'IngredientQuantity': quant_ingredient.quantity,
                'IngredientPrefix': quant_ingredient.prefix,
                'IngredientSuffix': quant_ingredient.suffix,
            }
            (qmarks, bindings) = sqlhelpers.insert_filler(
                constants.SQL_RECIPEINGREDIENT_COLUMNS,
                recipe_ingredient_data
            )
            query = 'INSERT INTO Recipe_Ingredient_Map VALUES(%s)' % qmarks
            cur.execute(query, bindings)

        self.recipedb.sql.commit()

class Review(ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_REVIEW_COLUMNS, db_row))

        self.id = db_row['ReviewID']
        self.author_id = db_row['AuthorID']
        self.recipe_id = db_row['RecipeID']
        self.date_added = db_row['DateAdded']
        self.score = db_row['Score']
        self.text = db_row['Text']

    def __repr__(self):
        return 'Review:%s on %s' % (self.id, self.recipe_id)

    def edit(self, score=None, text=None):
        if score is not None:
            score = int(score)
            self.recipedb._assert_valid_review_score(score)
            self.score = score

        if text is not None:
            self.text = text

        if not self.text and not self.score:
            raise ValueError('Text and score cannot both be blank')

        query = '''
        UPDATE Review SET Score = ?, Text = ?
        WHERE ReviewID = ?
        '''
        bindings = [self.score, self.text, self.id]
        cur = self.recipedb.sql.cursor()
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def get_author(self):
        return self.recipedb.get_user(id=self.author_id)

    def get_recipe(self):
        return self.recipedb.get_recipe(id=self.recipe_id)


#class User(ObjectBase):
class User(UserMixin, ObjectBase):
    def __init__(self, recipedb, db_row):
        super().__init__(recipedb)
        if isinstance(db_row, (list, tuple)):
            db_row = dict(zip(constants.SQL_USER_COLUMNS, db_row))

        self.id = db_row['UserID']
        self.username = db_row['Username']
        self.display_name = db_row['DisplayName']
        self.password_hash = db_row['PasswordHash']
        self.bio_text = db_row['BioText']
        self.date_joined = db_row['DateJoined']
        self.profile_image_id = db_row['ProfileImageID']

        if not self.display_name:
            self.display_name = self.username

        if not self.bio_text:
            self.bio_text = ''

    def __repr__(self):
        return 'User:%s:%s' % (self.id, self.username)

    def follow(self, other):
        if other == self:
            return

        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM User_Following_Map WHERE UserID = ? AND TargetID = ?', [self.id, other.id])
        if cur.fetchone() is not None:
            return

        data = {
            'UserID': self.id,
            'TargetID': other.id,
        }
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_USERFOLLOW_COLUMNS, data)
        query = 'INSERT INTO User_Following_Map VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.recipedb.sql.commit()

    def _get_following_followers(self, mycolumn):
        if mycolumn == 'UserID':
            query = 'SELECT TargetID FROM User_Following_Map WHERE UserID = ?'
        else:
            query = 'SELECT UserID FROM User_Following_Map WHERE TargetID = ?'

        cur = self.recipedb.sql.cursor()
        cur.execute(query, [self.id])
        user_ids = [f[0] for f in cur.fetchall()]
        users = [self.recipedb.get_user(id=i) for i in user_ids]
        return users

    def get_feed(self):
        '''
        Return a list containing the recipes and reviews published by the
        people I follow, sorted with most recent on top.
        '''
        feed_items = []
        for follow in self.get_following():
            feed_items.extend(follow.get_recipes())
            feed_items.extend(follow.get_reviews())

        feed_items.sort(key=lambda x: x.date_added, reverse=True)
        return feed_items

    def get_followers(self):
        return self._get_following_followers(mycolumn='TargetID')

    def get_following(self):
        return self._get_following_followers(mycolumn='UserID')

    def get_recipes(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Recipe WHERE AuthorID = ?', [self.id])
        rows = cur.fetchall()
        recipes = [Recipe(self.recipedb, row) for row in rows]
        recipes.sort(key=lambda x: x.date_added, reverse=True)
        return recipes

    def get_review_for_recipe(self, recipe):
        if isinstance(recipe, Recipe):
            recipe_id = recipe.id
        else:
            recipe_id = recipe
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Review WHERE AuthorID = ? AND RecipeID = ?', [self.id, recipe_id])
        review_row = cur.fetchone()

        if review_row is None:
            return None

        review = Review(self.recipedb, review_row)
        return review

    def get_reviews(self):
        cur = self.recipedb.sql.cursor()
        cur.execute('SELECT * FROM Review WHERE AuthorID = ?', [self.id])
        rows = cur.fetchall()
        reviews = [Review(self.recipedb, row) for row in rows]
        reviews.sort(key=lambda x: x.date_added, reverse=True)
        return reviews

    def set_bio_text(self, bio_text):
        if not isinstance(bio_text, (NoneType, str)):
            raise TypeError('bio_text should be None/str instead of %s.' % type(bio_text))

        cur = self.recipedb.sql.cursor()
        cur.execute('UPDATE User SET BioText = ? WHERE UserID = ?', [bio_text, self.id])
        self.recipedb.sql.commit()
        self.bio_text = bio_text

    def set_password(self, password):
        if not isinstance(password, (NoneType, str)):
            raise TypeError('password should be None/str instead of %s.' % type(password))

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = self.recipedb.sql.cursor()
        cur.execute('UPDATE User SET PasswordHash = ? WHERE UserID = ?', [password_hash, self.id])
        self.recipedb.sql.commit()
        self.password_hash = password_hash

    def set_display_name(self, display_name):
        if not isinstance(display_name, (NoneType, str)):
            raise TypeError('display_name should be None/str instead of %s.' % type(display_name))

        cur = self.recipedb.sql.cursor()
        cur.execute('UPDATE User SET DisplayName = ? WHERE UserID = ?', [display_name, self.id])
        self.recipedb.sql.commit()
        self.display_name = display_name

    def set_profile_image(self, image):
        cur = self.recipedb.sql.cursor()
        cur.execute('UPDATE User SET ProfileImageID = ? WHERE UserID = ?', [image.id, self.id])
        self.recipedb.sql.commit()
        self.profile_image_id = image.id

    def unfollow(self, other):
        if other == self:
            return

        # No need to check before deleting. If the row doesn't exist then who cares.
        cur = self.recipedb.sql.cursor()
        cur.execute('DELETE FROM User_Following_Map WHERE UserID = ? AND TargetID = ?', [self.id, other.id])
        self.recipedb.sql.commit()
