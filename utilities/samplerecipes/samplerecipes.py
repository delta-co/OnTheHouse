import recipedb

from voussoirkit import pathclass
image_dir = pathclass.Path(__file__).parent.with_child('sample_images')

rdb = recipedb.RecipeDB()

angela = rdb.new_user(
    username = "A",
    display_name = "Angela",
    password = "A",
    bio_text = "Hello! This is a sample biography for Angela.",
    profile_image = rdb.new_image(image_dir.with_child('angel_cake.jpg'))
)

bob = rdb.new_user(
    username = "B",
    display_name = "Bob",
    password = "A",
    bio_text = "Hello! This is a sample biography for Bob.",
    profile_image = rdb.new_image(image_dir.with_child('homemade_pizza.jpg'))
)

caitlyn = rdb.new_user(
    username = "C",
    display_name = "Caitlyn",
    password = "A",
    bio_text = "Hello! This is a sample biography for Caitlyn.",
    profile_image = rdb.new_image(image_dir.with_child('meringue.jpg'))
)

ethan = rdb.new_user(
    username='voussoir',
    display_name='Ethan Dalool',
    password='A',
    bio_text='Computer Science student who likes pizza.',
    profile_image=rdb.new_image(image_dir.with_child('voussoir.png'))
)

ian = rdb.new_user(
    username='ian',
    display_name='Ian Atol',
    password='I',
    bio_text='CS can stand for Computer Science or for Cooking Skills',
    profile_image=None
)

matt = rdb.new_user(
    username='matt',
    display_name='Matthew Haddad',
    password='M',
    bio_text='If Buzz Lightyear thinks he is a real space ranger, why is he still motionless when humans are around?',
    profile_image=None
)

panmomma = rdb.new_user(
    username='panmomma',
    display_name='Pan Momma',
    password='P',
    bio_text='Pan is life',
    profile_image=None
)

anonymous = rdb.new_user(
    username='anon',
    display_name='Rainbowman',
    password='A',
    bio_text='You cant touch me.',
    profile_image=None,
)

rdb.new_ingredient('egg', description='Laid by a chicken.')

def _child(parent, child):
    parent = rdb.get_or_create_ingredient_tag(parent)
    child = rdb.get_or_create_ingredient_tag(child)
    parent.add_child(child)

_child('meat', 'beef')
_child('meat', 'pork')
_child('meat', 'poultry')
_child('meat', 'fish')

def _tag(tagname, ingname):
    ing = rdb.get_or_create_ingredient(name=ingname)
    tag = rdb.get_or_create_ingredient_tag(tagname)
    ing.add_tag(tag)

_tag('chicken', 'roast chicken')
_tag('chicken', 'chicken broth')
_tag('chicken', 'chicken breast')

_tag('dairy', 'milk')
_tag('dairy', 'cheese')
_tag('dairy', 'cream cheese')
_tag('dairy', 'whipping cream')
_tag('dairy', 'butter')

_tag('flour', 'all-purpose flour')
_tag('flour', 'white flour')
_tag('flour', 'whole wheat flour')

_tag('rice', 'brown rice')
_tag('rice', 'sushi rice')
_tag('rice', 'white rice')

_tag('salt', 'sea salt')
_tag('salt', 'salt')

_tag('sugar', 'brown sugar')
_tag('sugar', 'cane sugar')
_tag('sugar', 'powdered sugar')
_tag('sugar', 'sugar')

def _autocorrect(tagname, alternate):
    tag = rdb.get_or_create_ingredient_tag(name=tagname)
    tag.add_autocorrect(alternate)

_autocorrect('potato', 'potatoes')
_autocorrect('egg', 'eggs')



# 1
instructions = '''
Soften cream cheese and Brie cheese.

For pesto, in a blender container combine basil, parsley, Parmesan cheese,
almonds, garlic, and 2 tablespoons oil. Cover; blend with on-off turns till a
paste forms. Gradually add remaining oil, blending on low speed till smooth.

Beat cream cheese and Brie together till nearly smooth. Beat whipping cream till
soft peaks form. Fold whipped cream into cheese mixture.

Line a 3 1/2- or 4-cup mold with plastic wrap. Spread one-fourth of cheese
mixture into mold. Top with one-third of pesto. Repeat layers twice. Top with
cheese mixture. Chill 6 to 24 hours.

To serve, unmold on plate. Remove plastic wrap. Garnish with fresh basil, if
desired. Serve with crackers.
'''
rdb.new_recipe(
    author=angela,
    blurb="This spread goes well with crackers or slided French bread.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','8-ounce package','cream cheese'),
        ('1','4 1/2-ounce package','Brie cheese'),
        ('1','cup firmly packed fresh','basil','leaves'),
        ('1/2','cup firmly packed','parsley','sprigs'),
        ('1/2','cup grated','Parmesan cheese'),
        ('1/4','cup','almond','s'),
        ('2','cloves','garlic',', quartered'),
        ('1/4','cup','olive oil'),
        ('1/2','cup','whipping cream')
    ],
    instructions=instructions,
    meal_type="Appetizer",
    name="Cheese and Pesto Spread",
    prep_time=10,
    serving_size=24,
    recipe_image=rdb.new_image(image_dir.with_child('cheese_pesto.jpg')),
)

# 2
blurb = '''
Need an egg dish for breakfast? Make these veggie stuffed omeletes that are
ready in just 15 minutes.
'''
instructions = '''
In 8-inch nonstick skillet, heat oil over medium-high heat. Add bell pepper,
onion and mushrooms to oil. Cook 2 minutes, stirring frequently, until onion is
tender. Stir in spinach; continue cooking and stirring just until spinach wilts.
Remove vegetables from pan to small bowl.

In medium bowl, beat egg product, water, salt and pepper with fork or whisk
until well mixed. Reheat same skillet over medium-high heat. Quickly pour egg
mixture into pan. While sliding pan back and forth rapidly over heat, quickly
stir with spatula to spread eggs continuously over bottom of pan as they
thicken. Let stand over heat a few seconds to lightly brown bottom of omelet.
Do not overcook; omelet will continue to cook after folding.

Place cooked vegetable mixture over half of omelet; top with cheese. With
spatula, fold other half of omelet over vegetables. Gently slide out of pan onto
plate. Serve immediately.
'''
rdb.new_recipe(
    author=bob,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','teaspoon','olive oil'),
        ('2','tablespoons chopped','red bell pepper'),
        ('1','tablespoon chopped','onion'),
        ('1/4','cup sliced','mushroom','s'),
        ('1','cup loosely packed fresh baby','spinach','leaves, rinsed'),
        ('2','','egg','s, beaten'),
        ('1','tablespoon','water'),
        ('','dash','salt'),
        ('','dash','pepper'),
        ('1','tablespoon shredded reduced-fat','Cheddar cheese')
    ],
    instructions=instructions,
    meal_type="Breakfast",
    name="Veggie Stuffed Omelete",
    prep_time=15,
    serving_size=1,
    recipe_image=rdb.new_image(image_dir.with_child('veggie_stuffed_omelette.jpg')),
)

# 3
blurb = '''
A great recipe for homemade pizza dough and sauce. The sauce is especially good.
Top with whatever you like.
'''
instructions = '''
In a small bowl, dissolve yeast in warm water.
Let stand until creamy, about 10 minutes.

In a large bowl, combine flour, salt and shortening. Stir in the yeast mixture.
When the dough has pulled together, turn it out onto a lightly floured surface,
and knead until smooth and elastic, about 8 minutes. Lightly oil a large bowl,
place the dough in the bowl, and turn to coat with oil. Cover with a damp cloth,
and let rise in a warm place until doubled in volume, about 45 minutes.

Heat oil in a small saucepan over medium heat. Saute onion until tender.
Stir in tomato paste and water. Season with sugar, salt, black pepper, garlic
powder, basil, oregano, marjoram, cumin, chili powder and red pepper flakes.
Simmer 15 to 20 minutes.

Recipe makes 2 (12 inch) pizzas. Divide dough in half, and spread onto pizza
pans. Cover with sauce, and desired toppings. Bake at 400 degrees for 20
minutes, or until crust is golden brown.
'''
rdb.new_recipe(
    author=caitlyn,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','envelope active dry','yeast'),
        ('1','cup lukewarm','water'),
        ('3','cups','all-purpose flour'),
        ('1/4','teaspoon','salt'),
        ('2','tablespoons','shortening'),
        ('1','tablespoon','vegetable oil'),
        ('1/2','cup chopped','onion'),
        ('1','can','tomato paste'),
        ('6','fluid ounces','water'),
        ('1/2','teaspoon','white sugar'),
        ('1/8','teaspoon','ground black pepper'),
        ('1/4','teaspoon','garlic powder'),
        ('1/4','teaspoon dried','basil'),
        ('1/4','teaspoon dried','oregano'),
        ('1/4','teaspoon dried','marjoram'),
        ('1/4','teaspoon','chili powder'),
        ('1/8','teaspoon crushed','red pepper flakes')
    ],
    instructions=instructions,
    meal_type="Anytime",
    name="Mike's Homemade Pizza",
    prep_time=90,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('homemade_pizza.jpg')),
)

# 4
instructions = '''
To make the churro dough: Combine 1 cup of water with the butter or margarine
and the salt in a saucepan and bring to a boil over high heat. Using a wooden
spoon, stir in flour. Reduce the heat to low and stir vigorously until the
mixture forms a ball, about 1 minute. Remove the dough from the heat and, while
stirring constantly, gradually beat the eggs into the dough.

To make the chocolate for dunking: In a small bowl, dissolve the cornstarch in
1 cup of milk and reserve. Combine the chocolate with the remaining cup of milk
in a saucepan. Stirring constantly, melt the chocolate over medium-low heat.
Whisk the sugar and the dissolved cornstarch into the melted chocolate mixture.
Reduce the heat to low and cook, whisking constantly, until the chocolate is
thickened, about 5 minutes. (Add extra cornstarch if it doesn't start to thicken
    after 5 minutes.) Remove the pan from the heat and whisk until smooth then
reserve in a warm place.

Heat about 2 inches of oil in a heavy, high-sided pot over medium-high heat
until the oil reaches 360 degrees F. Mix the sugar with the cinnamon on a plate
and reserve.

Meanwhile, spoon the churro dough into a pastry bag fitted with a large tip.
Squeeze a 4- inch strip of dough into the hot oil. Repeat, frying 3 or 4 strips
at a time. Fry the churros, turning them once, until golden brown, about 2
minutes per side. Transfer the cooked churros to a plate lined with paper towels
to drain.

When the churros are just cool enough to handle, roll them in the cinnamon-sugar
(in Spain churros are simply rolled in sugar.)

Pour the chocolate into individual bowls or cups. Serve the warm churros with
the chocolate dip.
'''
rdb.new_recipe(
    author=angela,
    blurb="Recipe courtesy of Chocolateria San Gines",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1', 'cup', 'water'),
        ('1/2', 'cup', 'butter'),
        ('1/4', 'teaspoon', 'salt'),
        ('1', 'cup', 'all-purpose flour'),
        ('3', '', 'egg', 's, beaten'),
        ('', '', 'vegetable oil', ', for frying'),
        ('1/4', 'cup', 'sugar'),
        ('1/4', 'teaspoon ground', 'cinnamon'),
        ('1', 'tablespoon', 'cornstarch'),
        ('2', 'cups', 'milk'),
        ('4', 'ounces', 'dark chocolate',', chopped'),
        ('1/4', 'cup', 'sugar')
    ],
    instructions=instructions,
    meal_type="Dessert",
    name="Churros",
    prep_time=40,
    serving_size=10,
    recipe_image=rdb.new_image(image_dir.with_child('churro.jpg')),
)

# 5
instructions = '''
Place a nori sheet lengthwise on a bamboo rolling mat, shiny-side down.
Position the sheet about 1-inch from the edge of the mat closest to you and
eave some of the bamboo mat exposed on either side of the nori sheet. Wet your
hands in cool water and take a handful of sushi rice. Place the rice in the
center of the nori and use your fingers to spread the rice evenly over the nori.
Be sure to leave a 3/4-inch strip of nori uncovered on the far side. Place tuna
strips and some julienne vegetable, cucumber or avocado along the center of the
rice. Be careful not to overfill the nori. Place your fingertips over the fillings
to hold them in place. Then, use your thumbs to lift up the edge of the bamboo
rolling mat closest to you. Begin rolling the mat away from you, while applying
pressure to the fillings to keep the roll firm. Roll the mat over slowly until
it covers the rice and the near and far sides of rice join, still leaving the
3/4-inch strip of nori, rice-free, exposed. While holding the bamboo mat in
position, apply pressure to the roll with your fingers to make the roll firm.
Slice the roll in half, then cut both rolls twice to make 6 equal sized pieces.
Repeat this process with the salmon and various fillings, nori and rice.

Rinse the rice in cold water while stirring briskly to remove any dirt. Drain
the rice completely. Place the rice and the 6 cups of water in a medium sized
saucepan and cover it with a tight fitting lid. Bring the water to a boil over
medium heat. Allow the water to boil for 3 minutes and then reduce the heat to
low and continue cooking 15 minutes without removing the lid. Remove the rice
from the heat and remove the lid (the water should no longer be visible). Turn
the rice out evenly on a well-greased cookie sheet using a spatula or rice
paddle. Sprinkle the rice with the vinegar, sugar, and salt while mixing with a
spatula or rice paddle until the rice reaches body temperature. Keep the rice
covered with damp paper towels or napkin until the rice is ready to use.
'''
rdb.new_recipe(
    author=bob,
    blurb="Recipe courtesy of Jill Davie",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('5','sheets','nori'),
        ('2','ounces sushi-grade','tuna',', cut into 1/4 by 1/2 by 3-inch strips'),
        ('2','ounces sushi-grade','salmon',', cut into 1/4 by 1/2 by 3-inch strips'),
        ('1','','hot house cucumber',', julienne'),
        ('1','','carrot',', peeled and julienne'),
        ('1/2','','avocado','thinly sliced'),
        ('5','cups short-grain','sushi rice'),
        ('6','cups','water'),
        ('1/2','cup','rice vinegar'),
        ('2','tablespoons','sugar'),
        ('1','teaspoon','salt')
    ],
    instructions=instructions,
    meal_type="Anytime",
    name="Sushi",
    prep_time=55,
    serving_size=30,
    recipe_image=rdb.new_image(image_dir.with_child('sushi.jpg')),
)

# 6
instructions = '''
Place a nori sheet lengthwise on a bamboo rolling mat, shiny-side down.
Position the sheet about 1-inch from the edge of the mat closest to you and
leave some of the bamboo mat exposed on either side of the nori sheet. Wet your
hands in cool water and take a handful of sushi rice. Place the rice in the
center of the nori and use your fingers to spread the rice evenly over the nori.
Be sure to leave a 3/4-inch strip of nori uncovered on the far side. Place tuna
strips and some julienne vegetable, cucumber or avocado along the center of the
rice. Be careful not to overfill the nori. Place your fingertips over the
fillings to hold them in place. Then, use your thumbs to lift up the edge of
the bamboo rolling mat closest to you. Begin rolling the mat away from you, while
applying pressure to the fillings to keep the roll firm. Roll the mat over
slowly until it covers the rice and the near and far sides of rice join, still
leaving the 3/4-inch strip of nori, rice-free, exposed. While holding the bamboo
mat in position, apply pressure to the roll with your fingers to make the roll
firm. Slice the roll in half, then cut both rolls twice to make 6 equal sized
ieces. Repeat this process with the salmon and various fillings, nori and rice.

Rinse the rice in cold water while stirring briskly to remove any dirt.
Drain the rice completely. Place the rice and the 6 cups of water in a medium
sized saucepan and cover it with a tight fitting lid. Bring the water to a boil
over medium heat. Allow the water to boil for 3 minutes and then reduce the heat
to low and continue cooking 15 minutes without removing the lid. Remove the rice
from the heat and remove the lid (the water should no longer be visible). Turn
the rice out evenly on a well-greased cookie sheet using a spatula or rice
paddle. Sprinkle the rice with the vinegar, sugar, and salt while mixing with a
spatula or rice paddle until the rice reaches body temperature. Keep the rice
covered with damp paper towels or napkin until the rice is ready to use.
'''
rdb.new_recipe(
    author=caitlyn,
    blurb="Recipe courtesy of Jill Davie",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('5','sheets','nori'),
        ('2','ounces sushi-grade','tuna',', cut into 1/4 by 1/2 by 3-inch strips'),
        ('2','ounces sushi-grade','salmon',', cut into 1/4 by 1/2 by 3-inch strips'),
        ('1','','hot house cucumber',', julienne'),
        ('1','','carrot',', peeled and julienne'),
        ('1/2','','avocado','thinly sliced'),
        ('5','cups short-grain','sushi rice'),
        ('6','cups','water'),
        ('1/2','cup','rice vinegar'),
        ('2','tablespoons','sugar'),
        ('1','teaspoon','salt')
    ],
    instructions=instructions,
    meal_type="Anytime",
    name="Sushi Rolls",
    prep_time=55,
    serving_size=30,
    recipe_image=rdb.new_image(image_dir.with_child('sushi_roll.jpg')),
)

# 7
blurb = '''
Sauerkraut is probably the most well-known lacto-fermented vegetable.
Like any traditionally homemade food, sauerkraut can be made in a number of
ways. Even if each kraut-making method is different there are a few common
basics to remember when fermenting sauerkraut at home.
'''
instructions = '''
Chop or shred cabbage. Sprinkle with salt.

Knead the cabbage with clean hands, or pound with a potato masher or Cabbage
Crusher about 10 minutes, until there is enough liquid to cover.

Stuff the cabbage into a quart jar, pressing the cabbage underneath the liquid.
If necessary, add a bit of water to completely cover cabbage.

Cover the jar with a tight lid, airlock lid, or coffee filter secured with a
rubber band.

Culture at room temperature (60-70F is preferred) for at least 2 weeks until
desired flavor and texture are achieved. If using a tight lid, burp daily to
release excess pressure.

Once the sauerkraut is finished, put a tight lid on the jar and move to cold
storage. The sauerkraut's flavor will continue to develop as it ages.
'''
rdb.new_recipe(
    author=angela,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','medium head of','cabbage'),
        ('2','tablespoons','sea salt')
    ],
    instructions=instructions,
    meal_type="Anytime",
    name="Homemade Sauerkraut",
    prep_time=10,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('sauerkraut.jpg')),
)

# 8
instructions = '''
In a large heavy saucepan mix eggs, milk, and 1/3 cup sugar. Cook and stir over
medium heat till mixture coats a metal spoon. Remove from heat. Cool quickly by
placing pan in a sink or bowl of ice water and stirring 1 to 2 minutes. Stir in
rum, bourbon, and vanilla. Chill 4 to 24 hours.

At serving time, in a bowl whip cream and 2 tablespoons sugar till soft peaks
form. Transfer chilled egg mixture to a punch bowl. Fold in whipped cream
mixture. Serve at once. Sprinkle each serving with nutmeg.
'''
rdb.new_recipe(
    author=bob,
    blurb="Always a hit at our annual staff Christmas party.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('6','beaten','egg','s'),
        ('2','cups','milk'),
        ('1/3','cup','sugar'),
        ('3','tablespoons','light rum'),
        ('3','tablespoons','bourbon'),
        ('1','teaspoon','vanilla'),
        ('1','cup','whipping cream'),
        ('2','tablespoons','sugar'),
        ('','ground','nutmeg')
    ],
    instructions=instructions,
    meal_type="Drink",
    name="Eggnog",
    prep_time=15,
    serving_size=10,
    recipe_image=rdb.new_image(image_dir.with_child('eggnog.jpg')),
)

# 9
instructions = '''
Preheat the oven to 350 F. Bring egg whites to room temperature. Sift powdered
sugar and flour together 3 times. In a large bowl beat egg whites, cream of
tartar, and vanilla with an electric mixer on medium speed till soft peaks form
(tips curl). Gradually add sugar, about 2 tablespoons at a time, beating till
stiff peaks form (tips stand straight).

Sift about one-fourth of the flour mixture over beaten egg whites; fold in
gently. (If bowl is too full, transfer to a larger bowl.) Repeat, folding in
remaining flour mixture by fourths.

Pour into an ungreased 10-inch tube pan. Bake on the lowest rack in a 350 F
oven for 40 to 45 minutes or until top springs back when lightly touched.
Immediately invert cake (leave in pan); cook thoroughly. Loosen sides of cake
from pan; remove cake.
'''
rdb.new_recipe(
    author=caitlyn,
    blurb="Eat your cake and diet, too. Angel Cake is low in calories and has no fat.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1 1/2','cups','egg white','s (10 to 12 large)'),
        ('1 1/2','cups sifted','powdered sugar'),
        ('1','cups sifted','all-purpose flour'),
        ('1 1/2','teaspoons','cream of tartar'),
        ('1','teaspoon','vanilla'),
        ('1','cup','sugar')
    ],
    instructions=instructions,
    meal_type="Dessert",
    name="Angel Cake",
    prep_time=60,
    serving_size=12,
    recipe_image=rdb.new_image(image_dir.with_child('angel_cake.jpg')),
)

# 10
blurb = '''
This recipe has been handed down from my mother.
It is a family favorite and will not be replaced! (Definite husband pleaser!)
'''
instructions = '''
Combine ground beef, onion, garlic, and green pepper in a large saucepan.
Cook and stir until meat is brown and vegetables are tender. Drain grease.

Stir diced tomatoes, tomato sauce, and tomato paste into the pan.
Season with oregano, basil, salt, and pepper. Simmer spaghetti sauce for 1 hour,
stirring occasionally.
'''
rdb.new_recipe(
    author=angela,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','pound ground','beef'),
        ('1','','onion',', chopped'),
        ('4','cloves','garlic',', chopped'),
        ('1','small','green bell pepper',', diced'),
        ('1','28-ounce can diced','tomato','es'),
        ('1','16-ounce can','tomato sauce'),
        ('1','6-ounce can','tomato paste'),
        ('2','teaspoons dried','oregano'),
        ('2','teaspoons dried','basil'),
        ('1','teaspoon','salt'),
        ('1/2','teaspoon','black pepper')
    ],
    instructions=instructions,
    meal_type="Dinner",
    name="Spaghetti Sauce with Ground Beef",
    prep_time=85,
    serving_size=6,
    recipe_image=rdb.new_image(image_dir.with_child('spaghetti_sauce.jpg')),
)

# 11
blurb = '''
This is a very fun recipe to follow, because Grandma makes it sweet and simple.
This pie is thickened with cornstarch and flour in addition to egg yolks, and
contains no milk.
'''
instructions = '''
Preheat oven to 350 degrees F (175 degrees C).

To Make Lemon Filling: In a medium saucepan, whisk together 1 cup sugar, flour,
cornstarch, and salt. Stir in water, lemon juice and lemon zest. Cook over
medium-high heat, stirring frequently, until mixture comes to a boil. Stir in
butter. Place egg yolks in a small bowl and gradually whisk in 1/2 cup of hot
sugar mixture. Whisk egg yolk mixture back into remaining sugar mixture.
Bring to a boil and continue to cook while stirring constantly until thick.
Remove from heat. Pour filling into baked pastry shell.

To Make Meringue: In a large glass or metal bowl, whip egg whites until foamy.
Add sugar gradually, and continue to whip until stiff peaks form. Spread
meringue over pie, sealing the edges at the crust.

Bake in preheated oven for 10 minutes, or until meringue is golden brown.
'''
rdb.new_recipe(
    author=bob,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1','cup','white sugar'),
        ('2','tablespoons','all-purpose flour'),
        ('3','tablespoons','cornstarch'),
        ('1/4','tablespoon','salt'),
        ('1 1/2','cups','water'),
        ('2','','lemon','s, juiced and zested'),
        ('2','tablespoons','butter'),
        ('4','','egg yolk','s, beaten'),
        ('1','9-inch','pie crust',', baked'),
        ('4','','egg white','s')
    ],
    instructions=instructions,
    meal_type="Dessert",
    name="Grandma's Lemon Meringue",
    prep_time=40,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('meringue.jpg')),
)

# 12
instructions = '''
Spritz 2 pieces of newspaper lightly with vegetable oil and place in the bottom
of a charcoal chimney starter. Fill the chimney starter with natural chunk
charcoal, 2 to 3 pounds, and set on the charcoal grate of a kettle grill until
hot and ashy, approximately 15 to 20 minutes.

Meanwhile, butter the bread slices on each side. Combine the cheeses, mustard,
paprika and pepper in small bowl.

Fold a long (24-inches) piece of heavy-duty aluminum foil in half. Set a large
metal griddle spatula in the center and fold the sides up around the spatula,
forming a tray. Spritz the spatula-tray with vegetable oil. Repeat with a second
piece of aluminum foil and another griddle spatula. Divide the cheese mixture
evenly between the spatula-trays, and set aside. Set aside two additional
15-inch sheets of heavy-duty aluminum foil.

Carefully and distribute the hot charcoal onto one side of the charcoal grate.
Set the cooking grate in place and heat for 2 to 3 minutes.

Set the cheese-filled spatula-trays on the grill over indirect heat. Cook for
6 to 9 minutes or until the cheese melts and bubbles around the edges. You may
have to adjust the placement of the spatula-trays to ensure even melting and
keep the cheese from overheating and breaking.

Grill the bread for 1 to 2 minutes per side over direct heat.

Place 1 slice of bread on each of the reserved sheets of aluminum foil. Pour
off excess grease into a bowl, if desired, then drizzle one spatula’s worth of
cheese onto one slice of bread and top with the a second slice of bread. Fold
the foil around the sandwich. Repeat with remaining cheese and bread slices,
and then return the sandwich packets to the grill over indirect heat for 1 to
2 minutes.

Unwrap and serve immediately.
'''
rdb.new_recipe(
    author=caitlyn,
    blurb="Not just a grilled cheese sandwich, but a grilled, grilled cheese sandwich.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('4','1/2-inch slices hearty','country bread'),
        ('1','ounce unsalted','butter',', at room temperature'),
        ('3','ounces grated extra sharp','Cheddar cheese'),
        ('3','ounces grated','Gruyere cheese'),
        ('1','teaspoon','dry mustard'),
        ('1/2','teaspoon smoked','paprika'),
        ('1/4','teaspoon freshly ground','black pepper')
    ],
    instructions=instructions,
    meal_type="Lunch",
    name="Grilled Grilled Cheese",
    prep_time=30,
    serving_size=2,
    recipe_image=rdb.new_image(image_dir.with_child('grilled_cheese.jpg')),
)

# 13
blurb = '''
If you love good, old fashioned mashed potatoes this is the perfect recipe.
Simple and delicious.
'''
instructions = '''
Bring a pot of salted water to a boil. Add potatoes and cook until tender but
still firm, about 15 minutes; drain.

In a small saucepan heat butter and milk over low heat until butter is melted.
Using a potato masher or electric beater, slowly blend milk mixture into
potatoes until smooth and creamy. Season with salt and pepper to taste.
'''
rdb.new_recipe(
    author=angela,
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('2','pounds baking','potato','es, peeled and quartered'),
        ('2','tablespoons','butter'),
        ('1','cup','milk'),
        ('','','salt','to taste'),
        ('','','pepper','to taste'),
    ],
    instructions=instructions,
    meal_type="Dinner",
    name="Basic Mashed Potatoes",
    prep_time=35,
    serving_size=4,
    recipe_image=rdb.new_image(image_dir.with_child('mashed_potatoes.jpg')),
)

# 14
instructions = '''
Cut margarine into thirds and bring it to room temperature. In the top of a
double boiler combine egg yoolk, water, lemon juice, pepper, and dash salt.
Add one piece of the margarine. Place over boiling water (upper pan should not
    touch water). Cook, stirring rapidly, till margarine melts and sauce begins
to thicken.

Add the remaining margarine, a piece at a time, stirring constantly. Cook and
stir till sauce thickens (1 to 2 minutes). Immediately remove from heat.
If sauce is too thick or curdles, immediately beat in 1 to 2 tablespoons hot
tap water. Serve the sauce with cooked vegetables, pultry, fish, or eggs.
'''
rdb.new_recipe(
    author=bob,
    blurb="A classic creamy sauce with a rich lemon flavor.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
        ('1/2','cup','margarine'),
        ('3','beaten','egg yolk','s'),
        ('1','tablespoon','water'),
        ('1','tablespoon','lemon juice'),
        ('','dash','white pepper')
    ],
    instructions=instructions,
    meal_type="Sauce",
    name="Hollandaise Sauce",
    prep_time=20,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('hollandaise.jpg')),
)

#v1
instructions = '''
Cut pork into strips. Heat sesame oil on medium heat.

Cook pork until brown, add can of coconut milk and bring to a boil.

Stir in red curry paste, hot chili oil, and brown sugar and simmer for 5 minutes

Add vegetables and simmer for 3 minutes, then stir in thai basil and fish sauce.

Serve with jasmine rice if desired.
'''
rdb.new_recipe(
    author=panmomma,
    blurb="This classic curry is great with any meat choice.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
      ('2 tbs', 'red curry paste'),
      ('13 oz','coconut milk'),
      ('2 tbs','fish sauce'),
      ('1 pound','pork'),
      ('2','bell pepper'),
      ('1 cup', 'bamboo shoots'),
      ('2 sprigs', 'thai basil'),
      ('2 tbs', 'sesame oil'),
      ('2 tbs', 'brown sugar'),
      ('1 tbs', 'hot chili oil')
    ],
    instructions=instructions,
    meal_type="Dinner",
    name="Thai Red Curry",
    prep_time=20,
    serving_size=6,
    recipe_image=rdb.new_image(image_dir.with_child('red_curry.jpg')),
)

#v2
instructions = '''
Mince mushrooms, cabbage, garlic and scallions.

Combine pork, mushrooms, cabbage, garlic, scallions soy sauce and mix by hand.
Grate in ginger and mix well.

In one hand hold gyoza skin and wet edges with water. Add 2 tsps of meat mixture
in center. As you fold over skins, pleat the edges to seal the gyoza.

Add sesame oil to pan and heat of medium high heat. Add gyoza to pan but
do not overcrowd them. Cook gyoza until bottoms start to brown, about 5 minutes.
Add 1/4 cup of water and place lid on pan. Steam for about 4 minutes

When gyoza are done, remove and serve with ponzu sauce and rice or enjoy as is.
'''
rdb.new_recipe(
    author=panmomma,
        blurb="Gyoza are also known as Japanese potstickers.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=[
      ('1 pound', 'ground','pork'),
      ('2 leaves','cabbage'),
      ('3','shitake mushroom'),
      ('2 tbs','grated','ginger'),
      ('2 tbs','soy sauce'),
      ('2','scallions'),
      ('2 cloves','garlic'),
      ('1 package','gyoza skins'),
      ('1 cup','water'),
      ('2 tbs','sesame oil')
    ],
    instructions=instructions,
    meal_type="Appetizer",
    name="Gyoza",
    prep_time=30,
    serving_size=6,
    recipe_image=rdb.new_image(image_dir.with_child('gyoza.jpg')),
)

#v3
instructions = '''
Add oil, peppercorns, bayleaves, cinnamon stick, and star anis in a
small pot over medium high heat.

Mince garlic and add to a heat resistant container(No plastic!!). Add in the
crushed red chilis,
salt, sesame oil, and black vinegar.

When the oil starts to bubble, place a wooden chopstick in oil, if bubbles form
around the chopstick
the oil is ready, if not, test chopstick every minute.

Gradually strain oil in container (very carefully!) and let sit for at least two
hours, 24 hours for best results.
Keep refridgerated for several months.

You can cook with this oil, add it to intant noodles, or use it as a sauce on
many dishes.
'''
rdb.new_recipe(
    author=panmomma,
    blurb="This recipe uses Chinese peppercorns which, in addition to being very spicy, can numb your mouth!",
    country_of_origin="China",
    cuisine="Unknown",
    ingredients=[
      ('1-1/2 cup','vegetable oil'),
      ('3/4 cup''crushed','red chili'),
      ('4-5''cloves of','garlic'),
      ('1 tsp','salt'),
      ('3 tbs','chinese peppercorn'),
      ('3','bayleaves'),
      ('1 stick', 'cinnamon'),
      ('4','star anis'),
      ('1 tsp','sesame oil' ),
      ('1 tsp','chinese black vinegar')
    ],
    instructions=instructions,
    meal_type="Sauce",
    name="Hot Chili Oil",
    prep_time=20,
    serving_size=40,
    recipe_image=rdb.new_image(image_dir.with_child('hot_chili_oil.jpg')),
)

#v4
instructions = '''
In a large bowl, sift together the flour, baking powder, salt and sugar.
Make a well in the center and pour in the milk, egg and melted butter; mix
until smooth.

Heat a lightly oiled griddle or frying pan over medium high heat. Pour or
scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.
Brown on both sides and serve hot.
'''
rdb.new_recipe(
    name='Fluffy Pancakes',
    author=panmomma,
    blurb='this is a family favorite.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 and 1/2 cups', 'all-purpose','flour'),
        ('1 tbs', 'granulated', 'sugar'),
        ('1 tsp', 'salt'),
        ('1 1/4 cup', 'milk'),
        ('3 Tbs', 'unsalted', 'butter'),
        ('1', 'large', 'egg'),
        ('3 1/2 tsps','baking powder'),
    ],
    instructions=instructions,
    serving_size=10,
    meal_type="breakfast",
    prep_time=20,
    recipe_image=rdb.new_image(image_dir.with_child('pancake.jpg')),
)

#v5
instructions = '''
Preheat oven to 350 degrees F (175 degrees C). Grease and flour a 9x5 inch pan.
Mash bananas.

Cream margarine and sugar until smooth. Beat in eggs, then bananas. Add flour
and soda,
stirring just until combined.

Pour into prepared pan and bake at 350 degrees F (175 degrees C) for about 1 hour
(or till toothpick comes out clean). Remove from pan and let cool, store in
refrigerator or freeze.
'''
rdb.new_recipe(
    name='Banana bread',
    author=panmomma,
    blurb='A classic recipe for those uneaten bananas',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 cups', 'all-purpose','flour'),
        ('1 cup', 'white', 'sugar'),
        ('2','ripe','bananas'),
        ('1/2 cup', 'margarine'),
        ('2', 'eggs'),
        ('1 tsps','baking soda'),
    ],
    instructions=instructions,
    serving_size=10,
    meal_type="Anytime",
    prep_time=75,
    recipe_image=rdb.new_image(image_dir.with_child('banana_bread.jpg')),
)

#v6
instructions = '''
Preheat oven to 350 degrees F (175 degrees C). Grease and flour a 9x13 inch pan.

In a large bowl, beat together eggs, oil, white sugar and 2 teaspoons vanilla.
Mix in flour, baking soda, baking powder, salt and cinnamon. Stir in carrots.
Fold in pecans. Pour into prepared pan.

Bake in the preheated oven for 40 to 50 minutes, or until a toothpick inserted
into the center of the cake comes out clean. Let cool in pan for 10 minutes,
then turn out onto a wire rack and cool completely.

To Make Frosting: In a medium bowl, combine butter, cream cheese, powdered
sugar and 1 teaspoon vanilla.
Beat until the mixture is smooth and creamy. Stir in chopped pecans. Frost
the cooled cake.
'''
rdb.new_recipe(
    name='Carrot Cake',
    author=panmomma,
    blurb='Dont even think of putting raisins in this',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 cups', 'all-purpose','flour'),
        ('2 cups', 'white', 'sugar'),
        ('3 cups','grated','carrots'),
        ('1 1/4 cups', 'vegetable oil'),
        ('4', 'eggs'),
        ('2 tsp','vanilla extract'),
        ('2 tsp','baking powder'),
        ('1/2 tsp','salt'),
        ('1 tsps','baking soda'),
        ('t tsps','ground','cinnamon'),
        ('1/2 cup','butter'),
        ('8 oz','cream cheese'),
        ('4 cups','powdered sugar'),
        ('1 tsp','vanilla extract'),
    ],
    instructions=instructions,
    serving_size=10,
    meal_type="Dessert",
    prep_time=120,
    recipe_image=rdb.new_image(image_dir.with_child('carrot_cake.jpg')),
)

#v7
instructions = '''
Preheat oven to 375 degrees F (175 degrees C). Grease an 8 inch square pan.

Melt butter in large skillet. Remove from heat and stir in sugar. Quickly add
eggs and beat until well blended. Combine buttermilk with baking soda and stir
into mixture in pan. Stir in cornmeal, flour, and salt until well blended and
few lumps remain. Pour batter into the prepared pan.

Bake in the preheated oven for 30 to 40 minutes, or until a toothpick inserted
in the center comes out clean.
'''
rdb.new_recipe(
    name='Corn Bread',
    author=panmomma,
    blurb='Sweet and delicious',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 cup', 'all-purpose','flour'),
        ('2/3 cup', 'white', 'sugar'),
        ('2', 'eggs'),
        ('1 cup','buttermilk'),
        ('1/2 tsp','salt'),
        ('1/2 tsps','baking soda'),
        ('1/2 cup','butter'),
        ('1 cup','corn meal'),
      ],
    instructions=instructions,
    serving_size=8,
    meal_type="Anytime",
    prep_time=55,
    recipe_image=rdb.new_image(image_dir.with_child('corn_bread.jpg')),
)

#v8
instructions = '''
Preheat the oven to 325 degrees F (165 degrees C).

In a large bowl, cream together the butter, brown sugar, and white sugar until
smooth.

Beat in eggs one at a time, then stir in vanilla. Combine the flour, baking
soda, and salt; stir into the creamed mixture until just blended. Mix in the
quick oats, walnuts, and chocolate chips. Drop by heaping spoonfuls onto
ungreased baking sheets.

Bake for 12 minutes in the preheated oven. Allow cookies to cool on baking
sheet for 5  minutes before transferring to a wire rack to cool completely.
'''
rdb.new_recipe(
    name='Oatmeal Chocolate Chip Cookies',
    author=panmomma,
    blurb='Why are raisins even a thing?',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 1/4 cup', 'all-purpose','flour'),
        ('1/2 cup', 'white', 'sugar'),
        ('2', 'eggs'),
        ('1 cup','butter'),
        ('1 tsp','salt'),
        ('1/2 tsps','baking soda'),
        ('3 cups','oats'),
        ('1 cup','semisweet','chocolate chips'),
        ('1 cup','brown','sugar'),
        ('2 tsps','vanilla extract'),
        ('1 cup','walnuts')
      ],
    instructions=instructions,
    serving_size=24,
    meal_type="Anytime",
    prep_time=55,
    recipe_image=rdb.new_image(image_dir.with_child('oatmeal_cookies.jpg')),
)

#v9
instructions = '''
Preheat oven to 400 degrees F (205 degrees C).

In a large bowl, beat eggs until foamy, and stir in melted butter. Stir in the
brown sugar,  white sugar and the flour; mix well. Last add the milk, vanilla
and nuts.

Pour into an unbaked 9-in pie shell. Bake in preheated oven for 10 minutes at
400 degrees, then reduce temperature to 350 degrees and bake for 30 to 40
minutes, or until done.
'''
rdb.new_recipe(
    name='Pecan Pie',
    author=panmomma,
    blurb='Unlike most pecan pies, this one does not require corn syrup.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 tbs', 'all-purpose','flour'),
        ('1/4 cup', 'white', 'sugar'),
        ('2', 'eggs'),
        ('1/2 cup','butter'),
        ('1/2 tbs','milk'),
        ('1 cup','brown','sugar'),
        ('1 tsps','vanilla extract'),
        ('1 cup','pecans')
      ],
    instructions=instructions,
    serving_size=8,
    meal_type="Anytime",
    prep_time=65,
    recipe_image=rdb.new_image(image_dir.with_child('pecan_pie.jpg')),
)

#v10
instructions = '''
Preheat oven to 350 degrees F (175 degrees C). Grease one 9 or 10 inch
tube/Bundt(R) pan.

Mix white sugar and cinnamon in a plastic bag. Cut biscuits into quarters.
Shake 6 to 8 biscuit
pieces in the sugar cinnamon mix. Arrange pieces in the bottom of the prepared
pan. Continue until  all biscuits are coated and placed in pan. If using nuts,
arrange them in and among the  biscuit pieces as you go along.

In a small saucepan, melt the margarine with the brown sugar over medium heat.
Boil for 1 minute.  Pour over the biscuits.

Bake at 350 degrees F (175 degrees C) for 35 minutes. Let bread cool in pan for
10 minutes, then turn
out onto a plate. Do not cut! The bread just pulls apart.
'''
rdb.new_recipe(
    name='Monkey Bread',
    author=panmomma,
    blurb='Easy to make, and will become any cinnamon-lovers favorite',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('3 packages','biscuit dough'),
        ('1 cup', 'white', 'sugar'),
        ('2 tsps','cinnamon'),
        ('1/2 cup','margarine'),
        ('1 cup','brown','sugar'),
        ('1/2 cup','walnuts')
      ],
    instructions=instructions,
    serving_size=8,
    meal_type="Anytime",
    prep_time=60,
    recipe_image=rdb.new_image(image_dir.with_child('monkey_bread.jpg')),
)


instructions = '''
Mix together egg, milk, salt, vanilla, and cinnamon or other spicesin a wide,
shallow bowl.

Prepare a lightly oiled skillet over medium-high heat.

Dip each slice of bread into the egg mixture, soaking thoroughly.

Place slice in pan and cook both sides.

Top with butter, powdered sugar, and maple syrup to preference. Serve.
'''
rdb.new_recipe(
    name='Easy French Toast',
    author=ethan,
    blurb='Quick, delicious breakfast.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('6 slices', 'thick', 'bread'),
        ('2', 'eggs'),
        ('2/3 cup', 'milk'),
        ('1/4 teaspoon', 'ground cinnamon'),
        ('1 teaspoon', 'vanilla extract'),
        ('A pinch of', 'salt'),
        'powdered sugar',
        'butter',
        'maple syrup',
    ],
    instructions=instructions,
    serving_size=3,
    meal_type='Breakfast',
    prep_time=20,
    recipe_image=rdb.new_image(image_dir.with_child('french_toast.jpg')),
)

instructions = '''
Peel potatoes.

Boil potatoes in salted water for 15 minutes. Potatoes should be cooked on the
outside but still stiff.

Dry on paper towels, and cut into slices.

Deep fry in hot oil until brown and crispy.

Dry, add salt, and serve.
'''
rdb.new_recipe(
    name='Family-fun French Fries',
    author=ethan,
    blurb='Make this night in feel like a night out.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('4', 'large', 'potatoes'),
        'frying oil',
        'salt',
    ],
    instructions=instructions,
    serving_size=3,
    meal_type='Anytime',
    prep_time=20,
    recipe_image=rdb.new_image(image_dir.with_child('french_fries.jpg')),
)

instructions = '''
Blend strawberries, banana, and yogurt in a blender.

Once smooth, add ice and blend again.

Pour, and top with whipped cream.
'''
rdb.new_recipe(
    name='Strawberry Banana Smoothie',
    author=ethan,
    blurb='Healthy and tasty smoothie to start your day.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1/2 cup', 'fresh chopped', 'strawberries'),
        ('1/4', 'peeled', 'banana'),
        ('1/4 cup', 'vanilla yogurt'),
        ('1/2 cup', 'crushed', 'ice'),
        'whipped cream',
    ],
    instructions=instructions,
    serving_size=1,
    meal_type='Drink',
    prep_time=10,
    recipe_image=rdb.new_image(image_dir.with_child('strawberry_banana_smoothie.jpg')),
)

instructions = '''
Preheat oven to 350 degrees F (175 degrees C). Grease and flour two 9 inch cake
pans.

Use the first set of ingredients to make the cake. In a medium bowl, stir
together the sugar, flour, cocoa, baking soda, baking powder and salt. Add the
eggs, milk, oil and vanilla, mix for 3 minutes with an electric mixer. Stir in
the boiling water by hand. Pour evenly into the two prepared pans.

Bake for 30 to 35 minutes in the preheated oven, until a toothpick inserted
comes out clean. Cool for 10 minutes before removing from pans to cool
completely.

To make the frosting, use the second set of ingredients. Cream butter until
light and fluffy. Stir in the cocoa and confectioners' sugar alternately with
the milk and vanilla. Beat to a spreading consistency.

Split the layers of cooled cake horizontally, cover the top of each layer with
frosting, then stack them onto a serving plate. Frost the outside of the cake.
'''
rdb.new_recipe(
    name='Very Chocolate Cake',
    author=ethan,
    blurb='Bye bye, diet.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 cups', 'white sugar'),
        ('1 and 3/4 cups', 'all-purpose flour'),
        ('3/4 cup', 'unsweetened', 'cocoa powder'),
        ('1 and 1/2 teaspoons', 'baking soda'),
        ('1 and 1/2 teaspoons', 'baking powder'),
        ('1 teaspoon', 'salt'),
        ('1/2 cup', 'vegetable oil'),
        ('2 teaspoons', 'vanilla extract'),
        ('1 cup', 'water'),
        ('3/4 cup', 'butter',),
        ('2', 'eggs'),
        ('1 cup', 'milk'),
    ],
    instructions=instructions,
    serving_size=1,
    meal_type='Dessert',
    prep_time=70,
    recipe_image=rdb.new_image(image_dir.with_child('chocolate_cake.jpg')),
)

instructions = '''
Put the bones and carcass from a leftover chicken (they can be in pieces) in a
large pot. Cover with the broth and 4 cups water. Bring to a boil over
medium-high heat, reduce to a simmer and cook for 20 minutes. Skim any foam or
fat from the broth with a ladle as necessary.

Remove the bones and carcass with tongs or a slotted spoon; set aside to cool.
Add the carrots, celery, onion and bay leaf to the broth, bring back to a simmer
and cook until the vegetables are about half cooked (they will still have
resistance when tested with a knife but be somewhat pliable when bent),
about 10 minutes. Stir in the rice (to keep it from sticking to the bottom),
and cook until the grains are just al dente, 10 to 12 minutes.

Meanwhile, when the carcass and bones are cool enough to handle, pick off the
meat, and shred it into bite-size pieces.

When the rice is done, add the meat to the broth and simmer until warmed
through, about 1 minute. Stir in the parsley, and season with 1/2 teaspoon salt
or more to taste. Serve hot.
'''
rdb.new_recipe(
    name='"Get Well Soon" Chicken Soup',
    author=ethan,
    blurb=None,
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('4 or 5 pounds', 'roast chicken'),
        ('4 cups', 'low-sodium', 'chicken broth'),
        ('2', 'sliced', 'carrots'),
        ('2 stalks', 'celery'),
        ('1', 'medium, chopped', 'onion'),
        ('1', 'bay leaf'),
        ('1/2 cup', 'white rice'),
        ('2 tablespoons', 'chopped', 'parsley'),
        'salt',
    ],
    instructions=instructions,
    serving_size=4,
    meal_type='Dinner',
    prep_time=55,
    recipe_image=rdb.new_image(image_dir.with_child('chicken_soup.jpg')),
)

instructions = '''
Preheat oven to 400 degrees F (200 degrees C). Line a baking sheet with
parchment paper or lightly grease.

Beat 1 1/2 cups white sugar, butter, and eggs together in a bowl using an
electric mixer until smooth and creamy. Combine flour, cream of tartar, baking
soda, and salt in a separate bowl; stir into creamed butter mixture until dough
holds together.

Mix 2 tablespoons white sugar and cinnamon together in a bowl.

Form dough into 2-teaspoon-size balls and roll in the cinnamon-sugar mixture.
Place dough balls, about 2 inches apart, on the prepared baking sheet.

Bake in the preheated oven on the center rack for 7 minutes. Allow cookies to
cool on the baking sheet for 5 minutes before transferring to a wire rack.
'''
rdb.new_recipe(
    name='Mom\'s Snickerdoodles',
    author=ethan,
    blurb='Just like mom used to make. But now you\'re making them.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 and 1/2 cups', 'white sugar'),
        ('1 cup', 'softened', 'butter'),
        ('2', 'eggs'),
        ('2 and 3/4 cups', 'all-purpose flour'),
        ('2 teaspoons', 'cream of tartar'),
        ('1 teaspoon', 'baking soda'),
        ('1/4 teaspoon', 'salt'),
        ('2 tablespoons', 'white sugar'),
        ('2 teaspoons', 'ground cinnamon'),
    ],
    instructions=instructions,
    serving_size=36,
    meal_type='Dessert',
    prep_time=35,
    recipe_image=rdb.new_image(image_dir.with_child('snickerdoodles.jpg')),
)

instructions = '''
Preheat oven to 375 degrees F (190 degrees C). Grease 24 mini-muffin cups.

Mix 1/2 cup sugar, 1/4 cup margarine, and nutmeg in a large bowl. Stir in the
milk, then mix in the baking powder and flour until just combined. Fill the
prepared mini muffin cups about half full.

Bake in the preheated oven until the tops are lightly golden, 15 to 20 minutes.

While muffins are baking, place 1/4 cup of melted margarine in a bowl. In a
separate bowl, mix together 1/2 cup of sugar with the cinnamon. Remove muffins
from their cups, dip each muffin in the melted margarine, and roll in the
sugar-cinnamon mixture. Let cool and serve.
'''
rdb.new_recipe(
    name='Donut Muffins',
    author=ethan,
    blurb='For when making that choice is just too hard.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1/2 cup', 'white sugar'),
        ('1/4 cup', 'melted', 'margarine'),
        ('3/4 teaspoon', 'ground nutmeg'),
        ('1/2 cup', 'milk'),
        ('1 teaspoon', 'baking powder'),
        ('1 cup', 'all-purpose flour'),
        ('1 teaspoon', 'ground cinnamon'),
    ],
    instructions=instructions,
    serving_size=24,
    meal_type='Dessert',
    prep_time=40,
    recipe_image=rdb.new_image(image_dir.with_child('donut_muffins.jpg')),
)

instructions = '''
Beat the eggs in a mixing bowl. Whisk in the milk, then set aside. Place the
bread crumbs into a plastic bag, and set aside.

Separate and place an egg roll wrapper onto your work surface with one of the
tips pointed towards you. Moisten the two far edges of the wrapper with water.
Place a string cheese stick onto the corner nearest you, and roll it in 1/3 of
the way, fold over the right and left corners, then continue rolling to the end,
pressing to seal. Repeat with the remaining string cheese sticks and egg roll
wrappers.

Heat oil in a deep-fryer or large saucepan to 375 degrees F (190 degrees C).

Dip the mozzarella sticks into the egg wash, then toss in the bread crumbs.
Cook in batches in the hot oil until crisp and golden brown, 3 to 4 minutes.
'''
rdb.new_recipe(
    name='Mozzarella Sticks',
    author=ethan,
    blurb='Sometimes all you need is a stick of cheese.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2', 'egg'),
        ('2 cups', 'milk'),
        ('1 and 1/2 cups', 'Italian seasoned', 'bread crumbs'),
        ('10', 'egg roll wrapper'),
        ('10 sticks', 'mozzarella cheese'),
        ('1 quart', 'frying oil'),
    ],
    instructions=instructions,
    serving_size=5,
    meal_type='Appetizer',
    prep_time=30,
    recipe_image=rdb.new_image(image_dir.with_child('mozzarella_sticks.jpg')),
)

instructions = '''
In a medium bowl, combine cornmeal, flour, salt, pepper, sugar and baking
powder. Stir in eggs and milk.

Preheat oil in a deep saucepan over medium heat. Insert wooden skewers into
frankfurters. Roll frankfurters in batter until well coated.

Fry 2 or 3 corn dogs at a time until lightly browned, about 3 minutes. Drain on
paper towels.
'''
rdb.new_recipe(
    name='Corn Dogs',
    author=ethan,
    blurb='It\'s like you\'re at the fair!',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 cup', 'yellow', 'cornmeal'),
        ('1 cup', 'all-purpose flour'),
        ('1/4 teaspoon', 'salt'),
        ('1/8 teaspoon', 'black pepper'),
        ('1/4 cup', 'white sugar'),
        ('4 teaspoons', 'baking powder'),
        ('1', 'egg'),
        ('1 cup', 'milk'),
        ('1 quart', 'frying oil'),
        ('16 ounces', 'beef frankfurters'),
        ('16', 'wooden', 'skewers'),
    ],
    instructions=instructions,
    serving_size=16,
    meal_type='Anytime',
    prep_time=40,
    recipe_image=rdb.new_image(image_dir.with_child('corn_dogs.jpg')),
)

instructions = '''
Make the dough: In a large bowl, mix the flour, the sugar, salt, and yeast
together until evenly dispersed. Set aside. In a small microwavable bowl, heat
the water, milk, and butter together in the microwave until the butter is melted
(about 30-45 seconds). Stir the butter mixture into the flour mixture. Add the
egg and knead with hand or with stand mixer for 3-4 minutes or until the dough
is no longer sticky. Place in a lightly greased bowl and let rest for about
5 minutes.

Preheat the oven to 200 degrees and turn off after 10 minutes or just before
placing rolls in oven.

Make the filling: After the dough has rested for 5 minutes, roll it out in a
15x9 inch rectangle. Spread the softened butter on top. Mix together the
cinnamon and sugar and sprinkle it all over the dough. Roll up the dough tightly
and cut into 9 (large) even piece. Place in a lightly greased 9-inch or square
pan (or cut into 12 small pieces and place in a 9x13 pan) and lightly cover
with aluminum foil or plastic wrap.

Turn off the oven and place the cinnamon buns in the oven to rise for 20
minutes. Keep the buns in the oven (REMOVE THE FOIL OR PLASTIC) and turn on
the oven to 375F. Bake the cinnamon rolls for 15-20 minutes or until golden.
Remove from oven and top with glaze.

Make the glaze: Mix the powdered sugar, vanilla and 2 Tablespoons milk together
until smooth and lump free. Drizzle over warm rolls.
'''
rdb.new_recipe(
    name='Homemade Cinnamon Rolls',
    author=ethan,
    blurb='Quick homehade cinnamon rolls from scratch.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 and 3/4 cups', 'all-purpose flour'),
        ('3 Tablespoons', 'granulated', 'sugar'),
        ('1 teaspoon', 'salt'),
        ('1/2 cup', 'water'),
        ('1/4 cup', 'milk'),
        ('2 Tablespoons', 'unsalted', 'butter'),
        ('1', 'large', 'egg'),
        ('1/4 cup', 'unsalted, softened', 'butter'),
        ('2 Tablespoons', 'ground cinnamon'),
        ('1/4 cup', 'brown sugar'),
        ('1 cup', 'powdered sugar'),
        ('1 teaspoon', 'vanilla extract'),
        ('2-3 Tablespoons', 'milk'),
    ],
    instructions=instructions,
    serving_size=9,
    meal_type='Breakfast',
    prep_time=45,
    recipe_image=rdb.new_image(image_dir.with_child('cinnamon_rolls.jpg')),
)

#ian 1
instructions = '''
Use paper towels to thoroughly dry excess moisture from fish fillets - this
step is crucial for fish to brown nicely in pan. Set aside.

In a bowl, combine melted butter, lemon juice and zest, and 1½ tsp kosher salt.
Stir to combine well. In a separate bowl, combine the remaining ½ tsp kosher
salt, paprika, garlic powder, onion powder, and black pepper.
Evenly press spice mixture onto both sides of fish fillets.

In a large, heavy pan over medium high heat, heat up the olive oil until hot.
Cook 2 fish fillets at a time to avoid overcrowding (allows for browning.)
Cook each side just until fish becomes opaque, feels somewhat firm in the center,
and is browned - lightly drizzle some of the lemon butter sauce as you cook,
reserving the rest for serving.
Take care not to over-cook, as that will result in a tougher texture.

Serve fish with with remaining lemon butter sauce, basil or parsley, and lemon
wedges.
'''
rdb.new_recipe(
    name='Easy Lemon Butter Fish',
    author=ian,
    blurb='Delicious and zesty',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('4', 'white fish fillets'),
        ('3 TB', 'melted butter'),
        ('1', 'lemon'),
        ('2 tsp', 'salt'),
        ('1 tsp', 'garlic powder'),
        ('1 tsp', 'onion powder'),
        ('1/4 tsp', 'ground', 'black pepper'),
        ('3 TB', 'olive oil'),
        ('1 tsp', 'onion powder'),
    ],
    instructions=instructions,
    serving_size=4,
    meal_type='Dinner',
    prep_time=19,
    recipe_image=rdb.new_image(image_dir.with_child('easy_lemon_butter_fish.jpg')),
)

#ian 2
instructions = '''
Let steaks stand 30 minutes at room temperature.

Sprinkle salt and pepper evenly over steaks. Heat a large cast-iron skillet
over high heat.
Add oil to pan; swirl to coat. Add steaks to pan; cook 3 minutes on each side
or until browned.
Reduce heat to medium-low; add butter, thyme, and garlic to pan. Carefully
grasp pan handle using an oven mitt or folded dish towel.
Tilt pan toward you so butter pools; cook 1 1/2 minutes, basting steaks with
butter constantly. Remove steaks from pan; cover loosely with foil.
Let stand 10 minutes. Reserve butter mixture.

Cut steak diagonally across grain into thin slices. Discard thyme and garlic;
spoon reserved butter mixture over steak.
'''
rdb.new_recipe(
    name='Pan Seared Strip Steak',
    author=ian,
    blurb='The three S\'s: Simple, Seared, and Steak. Oh, and Strip. 4 S\'s',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2', 'lean, grass-fed', 'strip steaks'),
        ('1 tbsp', 'salt'),
        ('3/4 tbsp', 'black pepper'),
        ('2 tsp', 'salt'),
        ('2 tsp', 'butter'),
        ('2 sprigs', 'thyme'),
        ('2 cloves', 'crushed', 'garlic'),
        ('1 tbsp', 'olive oil'),
    ],
    instructions=instructions,
    serving_size=6,
    meal_type='Dinner',
    prep_time=51,
    recipe_image=rdb.new_image(image_dir.with_child('seared_strip_steak.jpg')),
)

#ian 3
instructions = '''
Preheat oven to 350 degrees F (175 degrees C).


In a large bowl, combine the beef, egg, onion, milk and bread OR cracker crumbs.
Season with salt and pepper to taste and place in a lightly greased 5x9 inch
loaf pan, OR form into a loaf and place in a lightly greased 9x13 inch baking
dish.

In a separate small bowl, combine the brown sugar, mustard and ketchup.
Mix well and pour over the meatloaf.

Bake at 350 degrees F (175 degrees C) for 1 hour.
'''
rdb.new_recipe(
    name='Easy Meatloaf',
    author=ian,
    blurb='Easy and loafy',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 1/2 pounds', 'ground beef'),
        ('1', 'egg'),
        ('1', 'onion'),
        ('1 cup', 'milk'),
        ('1 cup', 'dried', 'bread crumbs'),
        ('2 tbsp', 'brown sugar'),
        ('2 tbsp', 'mustard'),
        ('1/3 cup', 'ketchup'),
    ],
    instructions=instructions,
    serving_size=8,
    meal_type='Dinner',
    prep_time=70,
    recipe_image=rdb.new_image(image_dir.with_child('easy_meatloaf.jpg')),
)

#ian 4
instructions = '''
Freeze the twinkies for at least 2 hours. Can freeze overnight.

Heat your oil in fryer to 375 degrees.

Mix your batter as such: milk, vinegar,oil.

In another bowl blend flour, baking powder and salt.

Whisk wet ingredients into dry, mix until smooth.

Refrigerate until oil reaches temperature.

Insert sticks into twinkies, leaving enough of a end to hold.

Dust with flour and dip into batter.
Be sure batter covers the entire twinkie place twinkie in hot oil with utensil.
Be sure the twinkie browns evenly (the twinkie will float) about 3- 4 minutes.

Remove to paper towel- cool 5 minutes.
Serve with a Berry Sauce Raspberries or mixed Berry preserves heated until warm.
Use for dipping.
'''
rdb.new_recipe(
    name='Fried Twinkies',
    author=ian,
    blurb='Fried and Twinky',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('6', 'twinkies'),
        ('6', 'wooden', 'popsicle sticks'),
        ('1 cup', 'vegetable oil'),
        ('1 cup', 'milk'),
        ('2 tbsp', 'vinegar'),
        ('1 cup', 'flour'),
        ('1 tbsp', 'baking powder'),
        ('1/2 teaspoon', 'salt'),
    ],
    instructions=instructions,
    serving_size=6,
    meal_type='Anytime',
    prep_time=15,
    recipe_image=rdb.new_image(image_dir.with_child('fried_twinkie.jpg')),
)

#ian 5
instructions = '''
Mix granulated sugar, cornstarch and nutmeg in 3-quart saucepan.

Gradually stir in milk.

Heat to boiling over medium heat, stirring constantly.

Boil and stir 1 minute; remove from heat.

Stir in butter and lemon peel.

Spread evenly in ungreased square baking dish, 8x8x2 inches.

Refrigerate uncovered at least 3 hours until firm.

Cut custard into 2-inch squares, using wet knife.

Dip custard squares into eggs, then coat with bread crumbs.

Heat oil (1 to 1/2 inches) to 360°F; fry 2 or 3 squares at a time in oil
1 to 2 minutes or until light brown; drain on paper towels.

Sprinkle with powdered sugar.
'''
rdb.new_recipe(
    name='Fried Milk',
    author=ian,
    blurb='Fried and Milky',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1/2 cup', 'granulated', 'sugar'),
        ('1/2 cup','cornstarch'),
        ('1/4 teaspoon', 'ground', 'nutmeg'),
        ('3 cups', 'milk'),
        ('1 tbsp', 'butter'),
        ('1/4 teaspoon', 'lemon rind'),
        ('2', 'eggs'),
        ('3/4 cup', 'breadcrumbs'),
        ('1/3 cup', 'powdered', 'sugar'),
    ],
    instructions=instructions,
    serving_size=8,
    meal_type='Anytime',
    prep_time=195,
    recipe_image=rdb.new_image(image_dir.with_child('fried_milk.jpg')),
)

#ian 6
instructions = '''
Make the batter by beating the eggs and sugar together.

Gradually add the milk and dry ingredients.

Preheat oil to 350°F.

Cook in hot vegetable oil until golden brown (a few minutes, depending on heat).

Cool on paper-towel covered tray for a few minutes, then dig in!
'''
rdb.new_recipe(
    name='Fried Kool-Aid',
    author=ian,
    blurb='Fried and Kool-Aidy',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('vegetable oil'),
        ('1/4 cup','Kool-Aid mix'),
        ('1/2 teaspoon', 'salt'),
        ('2 teaspoon', 'baking powder'),
        ('2 cups', 'milk'),
        ('3', 'eggs'),
        ('1/4 cup', 'sugar'),
        ('3 2/3 cup', 'flour'),
    ],
    instructions=instructions,
    serving_size=8,
    meal_type='Dessert',
    prep_time=7,
    recipe_image=rdb.new_image(image_dir.with_child('fried_koolaid.jpg')),
)

#ian 7
instructions = '''
Prepare lime, orange and 1 package of strawberry Jello as directed on the
packages.

Pour each flavor into separate 8-inch square pans.
Refrigerate 4 hours or until firm. Cut into 1/2 inch cubes; measure 1 1/2 cups
of each flavor.
(You can use the remaining cubes for garnish if desired, or for snacking).

Stir 1 cup boiling water into remaining package of lemon Jello in a medium bowl
until dissolved completely.
Stir in 1/2 cup cold water. Refrigerate 45 minutes or until slightly thickened
(consistency of unbeaten egg whites).

Stir in 1/2 of the Cool Whip. Gently stir in measured gelatin cubes.

Pour into a 9 x 5-inch loaf pan. Refrigerate overnight.

Unmold and garnish with remaining gelatin cubes and whipped topping, if desired.
'''
rdb.new_recipe(
    name='1950s Jello Dessert',
    author=ian,
    blurb='This retro dish is a tasty throwback!',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('1 package', 'lime Jell-O'),
        ('1 package', 'orange Jell-O'),
        ('1 package', 'strawberry Jell-O'),
        ('1 package', 'lemon Jell-O'),
        ('4 cups', 'boiling', 'water'),
        ('2 1/2 cups', 'cold', 'water'),
        ('1 container', 'Cool Whip'),
    ],
    instructions=instructions,
    serving_size=8,
    meal_type='Dessert',
    prep_time=1500,
    recipe_image=rdb.new_image(image_dir.with_child('1950s_jello.jpg')),
)

#ian 8
instructions = '''
Melt the butter in a medium frying pan over medium heat.
Add the flour and mix to form a paste, cooking it for 2 minutes.
Remove from the heat and let cool for 2 minutes, then gradually add the milk,
whisking continuously.

Place the pan back over medium heat; add the onion, clove, and bay leaf; and
simmer gently for 10 minutes, whisking frequently.
If the sauce becomes too thick, whisk in a little more milk 1 tablespoon at a
time until saucy.

Preheat the oven to 350°F.

Bring a stockpot of salted water to a boil.
Put the pasta in the water and cook for 2 minutes less than the package
instructions say.

Finish the sauce by removing the onion, clove, and bay leaf, then adding the
nutmeg and seasoning with salt and white pepper.
Stir in the mustard and half the cheese.

Drain the pasta and arrange the rigatoni pieces upright tightly in four
ovenproof dishes; they will look a bit like honeycomb.
Pour the sauce over the pasta. Tap the base of the baking dishes to allow the
sauce to get between the holes, spooning more on if necessary.
Place the mushroom stalks into the rigatoni holes, leaving the caps poking out.
Sprinkle with the remaining cheese.

Bake for 20 to 25 minutes, or until the cheese is golden and bubbling. Serve
with a sprinkle of finely chopped parsley on top.
'''
rdb.new_recipe(
    name='Cup Mushroom Pasta',
    author=ian,
    blurb='Totally trip out with this earthy dish',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 tbsp', 'butter'),
        ('1/4 cup', 'flour'),
        ('2 cups', 'milk'),
        ('1 clove', 'garlic'),
        ('1/4 cup', 'peeled', 'onion'),
        ('1', 'bay leaf'),
        ('9 ounces', 'pasta'),
        ('1 pinch', 'ground', 'nutmeg'),
        ('sea salt'),
        ('2 tbsp', 'mustard'),
        ('3 1/2 ounces', 'cheese'),
        ('6 ounces', 'mushrooms'),
        ('parsley'),
    ],
    instructions=instructions,
    serving_size=4,
    meal_type='Anytime',
    prep_time=30,
    recipe_image=rdb.new_image(image_dir.with_child('cup_mushroom_pasta.jpg')),
)

#ian 9
instructions = '''
Measure the tequila, lime juice, sweetened lime juice and triple sec into a
cocktail shaker and add a generous scoop of ice.

Cover and shake until the shaker is frosty, about 30 seconds.

Rub a lime wedge around the rim of a margarita glass and dip in salt.

Fill each glass with ice. Strain equal amounts of the cocktail into the glasses
to serve. Garnish with a lime wedge.
'''
rdb.new_recipe(
    name='Tasty Margarita',
    author=ian,
    blurb='Don\'t have too many of these delicious margaritas!',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('5 oz', 'tequila'),
        ('3 oz', 'lime juice'),
        ('3 oz', 'triple sec'),
        ('ice cubes'),
        ('1', 'lime'),
        ('salt'),
    ],
    instructions=instructions,
    serving_size=4,
    meal_type='Drinks',
    prep_time=5,
    recipe_image=rdb.new_image(image_dir.with_child('tasty_margarita.jpg')),
)

#ian 10
instructions = '''
Preheat an oven to 350 degrees F (175 degrees C).

Line a turkey roaster with long sheets of aluminum foil that will be long enough
to wrap over the turkey.

Stir together the parsley, rosemary, sage, thyme, lemon pepper, and salt in a
small bowl.

Rub the herb mixture into the cavity of the turkey, then stuff with the celery,
orange, onion, and carrot.
Truss if desired, and place the turkey into the roasting pan. Pour the chicken
broth and champagne over the turkey, making sure to get some champagne in the
cavity.

Bring the aluminum foil over the top of the turkey, and seal. Try to keep the
foil from touching the skin of the turkey breast or legs.

Bake the turkey in the preheated oven for 2 1/2 to 3 hours until no longer pink
at the bone and the juices run clear.
Uncover the turkey, and continue baking until the skin turns golden brown, 30
minutes to 1 hour longer.
An instant-read thermometer inserted into the thickest part of the thigh, near
the bone should read 180 degrees F (82 degrees C).
Remove the turkey from the oven, cover with a doubled sheet of aluminum foil,
and allow to rest in a warm area 10 to 15 minutes before slicing.
'''
rdb.new_recipe(
    name='Juicy Thanksgiving Turkey',
    author=ian,
    blurb='Just in time for the holidays.',
    country_of_origin=None,
    cuisine=None,
    ingredients=[
        ('2 tbsp', 'dried', 'parsley'),
        ('2 tbsp', 'ground', 'rosemary'),
        ('2 tbsp', 'dried' 'sage'),
        ('1 tbsp', 'lemon pepper'),
        ('1 tbsp', 'salt'),
        ('1', 'turkey'),
        ('2 stalks', 'celery'),
        ('1', 'orange'),
        ('1', 'onion'),
        ('1', 'carrot'),
        ('1 can', 'chicken broth'),
        ('1 bottle', 'champagne'),
    ],
    instructions=instructions,
    serving_size=20,
    meal_type='Dinner',
    prep_time=200,
    recipe_image=rdb.new_image(image_dir.with_child('juicy_turkey.jpg')),
)

import random
AGE_MAX = 30 * 24 * 60 * 60
now = recipedb.helpers.now()
cur = rdb.sql.cursor()
cur.execute('SELECT RecipeID FROM Recipe')
recipe_ids = [x[0] for x in cur.fetchall()]
for recipe_id in recipe_ids:
    created = now - random.randint(1, AGE_MAX)
    cur.execute('UPDATE Recipe SET DateAdded=? WHERE RecipeID=?', [created, recipe_id])
rdb.sql.commit()
