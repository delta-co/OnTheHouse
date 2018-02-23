import bcrypt
import copy
import json
import logging
import os
import sqlite3
import tempfile
import shutil

from . import constants
from . import exceptions
from . import helpers
from . import objects

from voussoirkit import pathclass
from voussoirkit import sqlhelpers

logging.basicConfig()


class RecipeDB:
    def __init__(
            self,
            data_directory=None,
        ):
        super().__init__()

        if data_directory is None:
            data_directory = constants.DEFAULT_DATADIR

        # DATA DIR PREP
        data_directory = helpers.remove_path_badchars(data_directory, allowed=':/\\')
        self.data_directory = pathclass.Path(data_directory)
        os.makedirs(self.data_directory.absolute_path, exist_ok=True)

        self.log = logging.getLogger('recipedb:%s' % self.data_directory.absolute_path)
        self.log.setLevel(logging.DEBUG)

        # DATABASE
        self.database_filepath = self.data_directory.with_child(constants.DEFAULT_DBNAME)

        existing_database = self.database_filepath.exists
        self.sql = sqlite3.connect(self.database_filepath.absolute_path)

        if not existing_database:
            self._first_time_setup()

        if existing_database:
            self._check_version()

        # CONFIG
        self.config_filepath = self.data_directory.with_child(constants.DEFAULT_CONFIGNAME)
        self.config = self._load_config()
        self.log.setLevel(self.config['log_level'])

        # IMAGE DIRECTORY
        self.image_directory = self.data_directory.with_child(constants.DEFAULT_IMAGEDIR)
        os.makedirs(self.image_directory.absolute_path, exist_ok=True)

        self.on_commit_queue = []

    def _check_version(self):
        '''
        This method is run on every init except the first time.
        Raises DatabaseOutOfDate if the user's database version is behind.
        '''
        cur = self.sql.cursor()

        cur.execute('PRAGMA user_version')
        existing_version = cur.fetchone()[0]
        if existing_version != constants.DATABASE_VERSION:
            exc = exceptions.DatabaseOutOfDate(
                current=existing_version,
                new=constants.DATABASE_VERSION,
            )
            raise exc

    def _first_time_setup(self):
        '''
        This method is run when the database is being created for the first
        time.
        '''
        self.log.debug('Performing first-time setup')

        cur = self.sql.cursor()
        statements = constants.DB_INIT.split(';')
        for statement in statements:
            cur.execute(statement)
        self.sql.commit()

    def _load_config(self):
        config = copy.deepcopy(constants.DEFAULT_CONFIGURATION)
        user_config_exists = self.config_filepath.is_file and self.config_filepath.size > 0
        if user_config_exists:
            with open(self.config_filepath.absolute_path, 'r') as handle:
                user_config = json.load(handle)
            my_keys = helpers.recursive_dict_keys(config)
            stored_keys = helpers.recursive_dict_keys(user_config)
            needs_dump = not my_keys.issubset(stored_keys)
            helpers.recursive_dict_update(config, user_config)
        else:
            needs_dump = True

        if (not user_config_exists) or needs_dump:
            with open(self.config_filepath.absolute_path, 'w') as handle:
                handle.write(json.dumps(config, indent=4, sort_keys=True))
        return config

    def _assert_valid_password(self, password):
        '''
        If something is wrong, raise an exception.
        Otherwise do nothing.
        '''
        if len(password) < constants.PASSWORD_MINLENGTH:
            raise exceptions.PasswordTooShort(minlength=constants.PASSWORD_MINLENGTH)

    def _assert_valid_username(self, name):
        '''
        If something is wrong, raise an exception.
        Otherwise do nothing.
        '''
        if len(name) < constants.USERNAME_MINLENGTH:
            raise exceptions.UsernameTooShort(name=name, minlength=constants.USERNAME_MINLENGTH)

        if len(name) > constants.USERNAME_MAXLENGTH:
            raise exceptions.UsernameTooLong(name=name, maxlength=constants.USERNAME_MAXLENGTH)

        badchars = set(character for character in name if character not in constants.USERNAME_CHARACTERS)

        if len(badchars) > 0:
            raise exceptions.InvalidUsernameCharacters(name=name, badchars=badchars)

    def _coerce_quantitied_ingredient(self, ingredient):
        '''
        Try to convert the given input to a QuantitiedIngredient.
        '''
        if isinstance(ingredient, objects.QuantitiedIngredient):
            return ingredient

        prefix = None
        suffix = None
        quantity = None

        if isinstance(ingredient, (tuple, list)):
            if len(ingredient) == 2:
                (quantity, ingredient) = ingredient
            elif len(ingredient) == 3:
                (quantity, prefix, ingredient) = ingredient
            elif len(ingredient) == 4:
                (quanitty, prefix, ingredient, suffix) = ingredient

        if isinstance(ingredient, dict):
            ingr = ingredient
            ingredient = ingr.get('ingredient', None)
            prefix = ingr.get('prefix', None)
            suffix = ingr.get('suffix', None)
            quantity = ingr.get('quantity', None)

        if isinstance(ingredient, str):
            ingredient = self.get_or_create_ingredient(name=ingredient)

        if isinstance(ingredient, objects.Ingredient):
            ingredient = objects.QuantitiedIngredient.from_existing(
                ingredient=ingredient,
                quantity=quantity,
                prefix=prefix,
                suffix=suffix,
            )

        if not isinstance(ingredient, objects.QuantitiedIngredient):
            raise TypeError('Type not recognized', ingredient)

        return ingredient

    def _normalize_ingredient_name(self, name):
        '''
        Apply any normalization rules that bring multiple equivalent forms
        of an ingredient name to a single, consistent form.
        '''
        name = name.strip()
        name = name.replace('_', ' ')
        return name

    def check_password(self, user, password):
        '''
        Check a typed password against the user's password
        '''
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, user.password_hash)

    def get_image(self, id):
        '''
        Fetch an image by its ID
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Image WHERE ImageID = ?', [id])
        image_row = cur.fetchone()
        if image_row is not None:
            image = objects.Image(self, image_row)
        else:
            raise ValueError('Image %s does not exist' % id)

        return image

    def get_or_create_ingredient(self, name):
        try:
            return self.get_ingredient(name=name)
        except exceptions.NoSuchIngredient:
            return self.new_ingredient(name)

    def get_or_create_ingredient_tag(self, name):
        try:
            return self.get_ingredient_tag(name=name)
        except exceptions.NoSuchIngredientTag:
            return self.new_ingredient_tag(name)

    def get_ingredient(self, *, id=None, name=None):
        '''
        Fetch a single Ingredient by its ID or name.
        '''
        if id is None and name is None:
            raise TypeError('id and name can\'t both be None.')

        if id is not None:
            ingredient = self.get_ingredient_by_id(id)
        else:
            ingredient = self.get_ingredient_by_name(name)

        return ingredient

    def get_ingredient_by_id(self, id):
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Ingredient WHERE IngredientID = ?', [id])
        ingredient_row = cur.fetchone()

        if ingredient_row is None:
            raise exceptions.NoSuchIngredient('ID: ' + id)

        ingredient = objects.Ingredient(self, ingredient_row)
        return ingredient

    def get_ingredient_by_name(self, name):
        name = self._normalize_ingredient_name(name)
        cur = self.sql.cursor()

        cur.execute('SELECT IngredientID FROM IngredientAutocorrect WHERE AlternateName = ?', [name])
        ingredient_row = cur.fetchone()

        if ingredient_row is not None:
            return self.get_ingredient_by_id(ingredient_row[0])

        cur.execute('SELECT * FROM Ingredient WHERE Name = ?', [name])
        ingredient_row = cur.fetchone()

        if ingredient_row is None:
            raise exceptions.NoSuchIngredient('Name: ' + name)

        ingredient = objects.Ingredient(self, ingredient_row)
        return ingredient

    def get_ingredient_tag(self, *, id=None, name=None):
        '''
        Fetch a single IngredientTag by its ID or name.
        '''
        if id is None and name is None:
            raise TypeError('id and name can\'t both be None.')

        if id is not None:
            tag = self.get_ingredient_tag_by_id(id)
        else:
            tag = self.get_ingredient_tag_by_name(name)

        return tag

    def get_ingredient_tag_by_id(self, id):
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM IngredientTag WHERE IngredientTagID = ?', [id])
        tag_row = cur.fetchone()

        if tag_row is None:
            raise exceptions.NoSuchIngredientTag('ID: ' + id)

        tag = objects.IngredientTag(self, tag_row)
        return tag

    def get_ingredient_tag_by_name(self, name):
        name = self._normalize_ingredient_name(name)

        cur = self.sql.cursor()
        cur.execute('SELECT * FROM IngredientTag WHERE TagName = ?', [name])
        tag_row = cur.fetchone()

        if tag_row is None:
            raise exceptions.NoSuchIngredientTag('Name: ' + name)

        tag = objects.IngredientTag(self, tag_row)
        return tag

    def get_recipe(self, id):
        '''
        Fetch a single Recipe by its ID.
        '''
        # SQL SELECT query and use row to construct Recipe object.
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Recipe WHERE RecipeID =?', [id])
        recipe_row = cur.fetchone()
        if recipe_row is not None:
            recipe = objects.Recipe(self, recipe_row)
        else:
            raise ValueError('Recipe %s does not exist' % id)

        return recipe

    def get_recipes(self):
        '''
        Returns all recipes
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM Recipe')
        recipe_rows = cur.fetchall()
        recipe_objects = [objects.Recipe(self, row) for row in recipe_rows]
        return recipe_objects

    def get_user(self, *, id=None, username=None):
        '''
        Fetch an user by their ID
        '''
        if id is None and username is None:
            raise TypeError('id and username can\'t both be None.')

        if id is not None:
            user = self.get_user_by_id(id)
        else:
            user = self.get_user_by_username(username)

        return user

    def get_user_by_id(self, id):
        '''
        Fetch an user by their ID
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM User WHERE UserID = ?', [id])
        user_row = cur.fetchone()

        if user_row is not None:
            user = objects.User(self, user_row)
        else:
            raise exceptions.NoSuchUser('ID:' + id)

        return user
    
    def get_user_by_username(self, username):
        '''
        Fetch an user by their username
        '''
        cur = self.sql.cursor()
        cur.execute('SELECT * FROM User Where Username = ?', [username])
        user_row = cur.fetchone()

        if user_row is not None:
            user = objects.User(self, user_row)
        else:
            raise exceptions.NoSuchUser('Name: ' + username)

        return user

    def new_image(self, filepath):
        '''
        Register a new image in the database.
        '''
        # generate id and generate new filepath based on id
        if isinstance(filepath, pathclass.Path):
            filepath = filepath.absolute_path

        id = helpers.random_hex()
        filetype = filepath.rsplit('.', 1)[1]
        new_filepath = '\\'.join(id[i:i + 4] for i in range(0, len(id), 4)) + '.' + filetype
        new_filepath = self.image_directory.join(new_filepath)
        os.makedirs(new_filepath.parent.absolute_path, exist_ok=True)
        new_filepath = new_filepath.absolute_path
        shutil.copyfile(filepath, new_filepath)
        data = {
            'ImageID': id,
            'ImageFilePath': new_filepath,
        }

        cur = self.sql.cursor()
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_IMAGE_COLUMNS, data)
        query = 'INSERT INTO Image VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.sql.commit()
        image = objects.Image(self, data)
        self.log.debug('Created image with ID: %s, filepath: %s' % (image.id, image.file_path))
        return image

    def new_ingredient(self, name, description=None, image=None):
        '''
        Add a new Ingredient to the database.
        '''
        name = self._normalize_ingredient_name(name)

        if image is not None:
            image_id = image.id
        else:
            image_id = None

        try:
            self.get_ingredient_by_name(name)
        except exceptions.NoSuchIngredient:
            pass
        else:
            raise exceptions.IngredientExists(name)

        cur = self.sql.cursor()

        data = {
            'IngredientID': helpers.random_hex(),
            'Name': name,
            'Description': description,
            'IngredientImageID': image_id,
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENT_COLUMNS, data)
        query = 'INSERT INTO Ingredient VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.sql.commit()

        ingredient = objects.Ingredient(self, data)
        self.log.debug('Created ingredient %s', ingredient.name)
        return ingredient

    def new_ingredient_tag(self, name, parent=None):
        '''
        Create a new IngredientTag, either a root or grouped under `parent`.
        '''
        name = self._normalize_ingredient_name(name)
        try:
            self.get_ingredient_tag_by_name(name)
        except exceptions.NoSuchIngredientTag:
            pass
        else:
            raise exceptions.IngredientTagExists(name)

        if parent is not None:
            parent_id = parent.id
        else:
            parent_id = None

        data = {
            'IngredientTagID': helpers.random_hex(),
            'TagName': name,
            'ParentTagID': parent_id,
        }

        cur = self.sql.cursor()
        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_INGREDIENTTAG_COLUMNS, data)
        query = 'INSERT INTO IngredientTag VALUES(%s)' % qmarks
        cur.execute(query, bindings)
        self.sql.commit()

        tag = objects.IngredientTag(self, data)
        self.log.debug('Created IngredientTag %s', tag.name)
        return tag

    def new_recipe(
            self,
            *,
            author: objects.User,
            blurb: str,
            country_of_origin: str,
            cuisine: str,
            ingredients: list,
            instructions: str,
            meal_type: str,
            name: str,
            prep_time: int,
            serving_size: int,
            recipe_image: objects.Image,
        ):
        '''
        Add a new recipe to the database.

        author: May be a string representing the author's ID, or a User object.
        ingredients: A list of either ingredient's ID, or Ingredient objects.
        '''
        cur = self.sql.cursor()

        recipe_id = helpers.random_hex()

        if author is not None:
            author_id = author.id
        else:
            author_id = None

        if instructions is not None:
            instructions = instructions.replace('\r', '')

        if recipe_image is not None:
            recipe_image_id = recipe_image.id
        else:
            recipe_image_id = None

        recipe_data = {
            'RecipeID': recipe_id,
            'Name': name,
            'AuthorID': author_id,
            'CountryOfOrigin': country_of_origin,
            'MealType': meal_type,
            'Cuisine': cuisine,
            'PrepTime': prep_time,
            'DateAdded': helpers.now(),
            'DateModified': helpers.now(),
            'Blurb': blurb,
            'ServingSize': serving_size,
            'Instructions': instructions,
            'RecipeImageID': recipe_image_id,
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_RECIPE_COLUMNS, recipe_data)
        query = 'INSERT INTO Recipe VALUES(%s)' % qmarks
        cur.execute(query, bindings)

        ingredients = [self._coerce_quantitied_ingredient(ingredient) for ingredient in ingredients]

        for quant_ingredient in ingredients:
            recipe_ingredient_data = {
                'RecipeID': recipe_id,
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

        self.sql.commit()

        recipe = objects.Recipe(self, recipe_data)
        self.log.debug('Created recipe %s', recipe.name)
        return recipe

    def new_user(
            self,
            username: str,
            password: str,
            *,
            display_name: str=None,
            bio_text: str=None,
            profile_image: objects.Image=None,
        ):
        '''
        Register a new User to the database
        '''
        self._assert_valid_username(username)
        self._assert_valid_password(password)

        try:
            self.get_user(username=username)
        except exceptions.NoSuchUser:
            pass
        else:
            raise exceptions.UserExists(username)

        cur = self.sql.cursor()

        user_id = helpers.random_hex()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        date_joined = helpers.now()

        if not display_name:
            display_name = username

        if not bio_text:
            bio_text = ''

        if profile_image is not None:
            profile_image_id = profile_image.id
        else:
            profile_image_id = None

        user_data = {
            'UserID': user_id,
            'Username': username,
            'DisplayName': display_name,
            'PasswordHash': password_hash,
            'BioText': bio_text,
            'DateJoined': date_joined,
            'ProfileImageID': profile_image_id,
        }

        (qmarks, bindings) = sqlhelpers.insert_filler(constants.SQL_USER_COLUMNS, user_data)
        query = 'INSERT INTO User VALUES(%s)' % qmarks
        cur.execute(query, bindings)

        self.sql.commit()

        user = objects.User(self, user_data)
        self.log.debug('Created user %s with ID %s', user.username, user.id)
        return user

    def _get_ingredient_or_tag(self, name):
        try:
            return self.get_ingredient(name=name)
        except exceptions.NoSuchIngredient:
            pass

        try:
            return self.get_ingredient_tag(name=name)
        except exceptions.NoSuchIngredientTag:
            pass

        return None

    def _normalize_ingredient_set(self, ingredients):
        '''
        When the user searches for a recipe, they might be providing us with
        a variety of data.
        '''
        if ingredients is None:
            return None

        elif not ingredients:
            return set()

        if isinstance(ingredients, str):
            ingredients = [i.strip() for i in ingredients.split(',')]
            ingredients = [i for i in ingredients if i]

        final_ingredients = set()
        for ingredient in ingredients:
            if isinstance(ingredient, str):
                ingredient = self._get_ingredient_or_tag(name=ingredient)
                if ingredient is not None:
                    final_ingredients.add(ingredient.name)
            if isinstance(ingredient, (objects.Ingredient, objects.IngredientTag)):
                final_ingredients.add(ingredient.name)
        return final_ingredients

    def search(
            self,
            *,
            author=None,
            country=None,
            cuisine=None,
            ingredients=None,
            ingredients_exclude=None,
            limit=None,
            meal_type=None,
            name=None,
            strict_ingredients=False,
        ):
        wheres = []
        bindings = []

        if author is not None:
            wheres.append('AuthorID = ?')
            bindings.append(author.id)

        if country is not None:
            wheres.append('Country = ?')
            bindings.append(country)

        if cuisine is not None:
            wheres.append('Cuisine = ?')
            bindings.append(cuisine)

        ingredients = self._normalize_ingredient_set(ingredients)
        ingredients_exclude = self._normalize_ingredient_set(ingredients_exclude)

        if meal_type is not None:
            wheres.append('MealType = ?')
            bindings.append(meal_type)

        if name is not None:
            wheres.append('Name LIKE ?')
            bindings.append('%' + name + '%')

        if wheres:
            wheres = ' AND '.join(wheres)
            wheres = 'WHERE ' + wheres
        else:
            wheres = ''

        cur = self.sql.cursor()
        query = 'SELECT * FROM Recipe {wheres}'
        query = query.format(wheres=wheres)
        self.log.debug("%s %s", query, bindings)
        cur.execute(query, bindings)

        match_counts = {}
        while True:
            recipe_row = cur.fetchone()
            if recipe_row is None:
                break

            recipe = objects.Recipe(self, recipe_row)
            recipe_ingredients = recipe.get_ingredients_and_tags()
            recipe_ingredients = {i.name for i in recipe_ingredients}

            if ingredients_exclude is not None:
                if recipe_ingredients.intersection(ingredients_exclude):
                    continue

            if ingredients is not None:
                matches = recipe_ingredients.intersection(ingredients)

                if not matches:
                    continue

                matched_all = matches == ingredients
                if strict_ingredients and not matched_all:
                    continue

                match_counts[recipe] = len(matches)

            else:
                match_counts[recipe] = 1

            if limit is not None and len(match_counts) >= limit:
                break

        results = sorted(match_counts.keys(), key=match_counts.get, reverse=True)

        return results
