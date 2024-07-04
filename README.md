This is a new project I'm working on as an alternative to other automated ways of rolling loot for your typical TTRPGs.

My end goal is to provide an automated way of generating loot hordes for a variety of situations, but also with certain features I have in mind for later.

Features I'm considering:
    1. Generating multiple hordes at a time, ideally in the context of a dungeon (so some poorer and some wealther hordes)
    2. Generating contextualized hordes based on specific keywords
    3. Possibly using monster subtypes as keywords with which to generate appropriate loot
    4. Generating terrain and points of interest for a hex map, starting either in an arbitrary corner or spiraling out from a center point
    5. Have CLI to interact with as it prompts you for input

As of now, just running the program will demo the functions I already have in decent shape. As of now it will:
    1. Import the equipment and terrain tables from the table folder
    2. Print out some filtered tables (only consumables for example)
    3. Do some random rolls for a couple tables
    4. Export the equipment, terrain and loot tables, and back up the old versions.

You can also edit it and just mess with the commands at the bottom to try out different filters and rolls.
Also, the tables are completely editable as long as you use the right format, and if you want you can use the createItem function in the terminal to make some as well.