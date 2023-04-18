# MatchingGame

Tools: Python, Pygame

The aim of the game is to find all the pairs with the fewest tries.
The user will start the program from a terminal window and specify the following command line arguments:
- color (required argument):  this is the color to be used for the matched tiles.  The only valid options are blue, green and magenta.
- image folder:  this is the name of a folder/directory that contains at least 8 images(.gif) to be used in the game. 
- fast option: The user can specify -f or --fast, or omit this option.  When the fast option is omitted, the delay before the images disappear is 3 seconds.  With the fast option, the delay is only 1 second.
e.g. python matchit.py green SJSUimages -f 

The score stays at 100 while the player flips the first 13 pairs of tiles.  For each additional pair of tiles flipped, the player will lose 10 points.

<img width="451" alt="Screen Shot 2023-04-12 at 1 42 04 PM" src="https://user-images.githubusercontent.com/71808318/231580004-f733f991-a082-4b36-8f49-88b5a8344303.png">

Demo link: https://drive.google.com/file/d/1VygPe2GabYfA6zkasajAUUuYOwDC-h3N/view?usp=sharing
