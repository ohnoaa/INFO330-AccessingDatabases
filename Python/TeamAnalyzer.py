import functools
import operator
import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters
connection = sqlite3.connect("../pokemon.sqlite")
con = connection.cursor()


# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    print("Analyzing " + arg)

    # Making variables for name and types
    pokemonName = con.execute("SELECT name FROM pokemon WHERE pokedex_number = " + arg).fetchone()
    pokemonNameString = functools.reduce(operator.add, pokemonName)

    pokemonType1 = con.execute("SELECT type1 FROM pokemon_types_view JOIN pokemon ON pokemon_types_view.name = pokemon.name WHERE pokedex_number = " + arg).fetchone()
    pokemonType1String = functools.reduce(operator.add, pokemonType1)

    pokemonType2 = con.execute("SELECT type2 FROM pokemon_types_view JOIN pokemon ON pokemon_types_view.name = pokemon.name WHERE pokedex_number = " + arg).fetchone()
    pokemonType2String = functools.reduce(operator.add, pokemonType2)


    # Finding all the against information (in that row)
    pokemonAgainst = con.execute("SELECT * FROM pokemon_types_battle_view WHERE type1name = '" + pokemonType1String + "' AND type2name = '" + pokemonType2String + "'").fetchmany()

    # Change the tuple into a list
    pokemonAgainstList = pokemonAgainst[0]

    # Getting rid of the type indexes
    pokemonAgainstNoType = pokemonAgainstList[2:21]

    # Making lists for strong and weak
    strongAgainst = []

    weakAgainst = []

    # Somehow save the values that are less and greater than 1 / Take all the values in against and see which are greater than 1 and less than 1
    # Use if statements here
    for i in range(len(pokemonAgainstNoType)):
        if pokemonAgainstNoType[i] > 1:
            # if pokemonAgainst[i] > 1:
            strongAgainst.append(types[i]) # use the type assignment with its index in the list
        elif pokemonAgainstNoType[i] < 1:
                weakAgainst.append(types[i])
        else:
                pass
        
        
    # Print out the results
    print(pokemonNameString + " (" + pokemonType1String + " " + pokemonType2String + ") is strong against ", strongAgainst, " but weak against ", weakAgainst)

    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")