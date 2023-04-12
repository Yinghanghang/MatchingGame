# MatchingGame

When the player clicks on a tile, the image associated with that tile is revealed.  The player will flip two tiles by clicking on them one after the other with the goal of finding a matching pair.   If the two images are different,  they are both hidden after a delay.  If the two images match, they are also hidden after a delay and the  corresponding tiles change color to a user specified color.  The game ends when all the images have been matched and the whole grid is colored with the user specified color.
The user will start the program from a terminal window and specify the following command line arguments:
- color (required argument):  this is the color to be used for the matched tiles.  The only valid options are blue, green and magenta.
- image folder:  this is the name of a folder/directory that contains at least 8 images(.gif) to be used in the game. 
- fast option: The user can specify -f or --fast, or omit this option.  When the fast option is omitted, the delay before the images disappear is 3 seconds.  With the fast option, the delay is only 1 second.
e.g. python matchit.py green SJSUimages -f 

The score stays at 100 while the player flips the first 13 pairs of tiles.  For each additional pair of tiles flipped, the player will lose 10 points.

<img width="453" alt="Screen Shot 2023-04-12 at 1 34 42 PM" src="https://user-images.githubusercontent.com/71808318/231578240-dac7a210-ba18-4ebb-a66f-59b39a9ceae0.png">
