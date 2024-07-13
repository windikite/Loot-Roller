This is a new project I'm working on as an alternative to other automated ways of rolling loot for your typical TTRPGs.  

My end goal is to provide an automated way of generating loot hordes for a variety of situations, but also with certain features I have in mind for later.  

Features I'm considering:  
    1. ~~Generating multiple hordes at a time, ideally in the context of a dungeon (so some poorer and some wealther hordes)~~    
    2. Generating contextualized hordes based on specific keywords  
    3. Possibly using monster subtypes as keywords with which to generate appropriate loot  
    4. Generating terrain and points of interest for a hex map, starting either in an arbitrary corner or spiraling out from a center point  
    5. ~~Have CLI to interact with as it prompts you for input~~

As of now, just running the program will provide a CLI for you to interact with in the terminal. As of now it will:  
    1. Import tables from the table folder to roll off of 
    2. Prompt you to either roll items(or item hordes!), view items (not working yet) or backup files  
    3. Prompt you to save your loot to a txt file 
  
Also, the tables are completely editable as long as you use the right format, and if you want you can create and delete items as well!.

Here is a walkthrough for creating and exporting a few loot hordes:
    1. Enter 6 into the terminal and press enter, choosing the "Roll loot" operation.  
    2. Enter 3 into the terminal and press enter, choosing the "Roll loot horde" operation.
    3. Enter the number of hordes you want to roll and press enter, whole numbers only (positive integers).  
    4. It will now ask you to specify the Loot Profile (settings) for each horde, as well as the amount of wealth in gold pieces to try and roll. 
    5. Once generated it will ask if you want to export to file; if you do, it will be in the loot.txt file!
