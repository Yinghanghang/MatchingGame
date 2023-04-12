"""
A single player matching game.

usage: matchit.py [-h] [-f] {blue,green,magenta} [image_folder]
positional arguments:
  {blue,green,magenta}  What color would you like for the player?
  image_folder          What folder contains the game images?

optional arguments:
  -h, --help            show this help message and exit
  -f, --fast            fast or slow game?
"""
import tkinter
import os
import random
import argparse


class MatchGame(object):
    """
    GUI Game class for a matching game.

    Arguments:
    parent: the root window object
    player_color (string): the color to be used for the matched tiles
    folder (string) the folder containing the images for the game
    delay (integer) how many milliseconds to wait before flipping a tile

    Attributes:
    canvas (tkinter.Canvas): the widget defining the area to be selected
    status (tkinter.Label): the widget showing score and game messages
    color (string): the paint color selected - blue, green or magenta
    tries (int): the number of pairs flipped by the user
    pair_match (int): the number of pairs matches
    score (int): player's score
    image_per_round (int): the number of images revealed per round
    delay (int): a period of time before the images disappear
    image_names (list): a list contains 16 image names
    image_dict (dict): a dictionary that maps each image name
                       to a tkinter.PhotoImage
    """

    # class variables
    canvas_size = 450
    canvas_color = "white"

    def __init__(self, parent, player_color, folder, delay):
        parent.title('Match it!')

        # Create the restart button widget
        restart_button = tkinter.Button(parent, text='RESTART',
                                        width=10,
                                        command=self.restart)
        restart_button.grid()  # register it with a geometry manager

        # Create a canvas widget
        self.canvas = tkinter.Canvas(parent, width=self.canvas_size,
                                     height=self.canvas_size,
                                     background=self.canvas_color)
        self.canvas.grid()  # register it with a geometry manager

        # instance variables
        self.score = 100  # player's score
        self.delay = 1000 if delay else 9000  # flip delay
        self.color = player_color  # user defined color

        # Create a list containing the valid image names
        folder_images = [file for file in os.listdir(folder) if
                         file.endswith(".gif")][:8]
        self.image_names = 2 * folder_images

        # Create a dictionary that maps each image name
        # to a tkinter.PhotoImage
        self.image_dict = {file: tkinter.PhotoImage(file=os.path.join(
            folder, file)) for file in folder_images}

        # Create a label widget for the score
        self.status = tkinter.Label(parent, text=f'Score: {self.score}')
        self.status.grid()

        # Call the restart method to finish the initialization
        self.restart()

        # When the user clicks on the canvas, invoke self.flip
        self.canvas.bind("<Button-1>", self.flip)

    def restart(self):
        """
        This method is invoked when player clicks on the RESTART button.
        It should also be called from __init__ to initialize the game.
        It shuffles and reassigns the images and resets the GUI and the
        score.
        :return: None
        """
        # initialize / reset the instance variables
        self.score = 100
        self.tries = 0         # number of pairs flipped
        self.images_per_round = 0  # number of image revealed per round
        self.pair_match = 0  # number of pairs matched

        # Reset label
        self.status.configure(text=f'Score: {self.score}')

        # Delete 'selected' tags on tiles to handel the case that
        # restart button is clicked before image(s) disappear (before
        # self.hide is called)
        selected_tiles = self.canvas.find_withtag('selected')
        for tile in selected_tiles:
            self.canvas.dtag(tile, 'selected')

        # Shuffles and reassigns the images
        random.shuffle(self.image_names)

        # Create 16 tiles
        index = 0
        for x in range(0, 448, 112):
            for y in range(0, 448, 112):
                # Create the tiles with an assigned image in the tag
                self.canvas.create_rectangle(x, y, x + 112, y + 112,
                                             fill='white',
                                             tags=self.image_names[index])
                index += 1

    def flip(self, event):
        """
        This method is invoked when the user clicks on a square.
        It implements the basic controls of the game.
        :param event: event (Event object) describing the click event
        :return: None
        """
        current_tags = self.canvas.gettags(tkinter.CURRENT)

        # Create tags for current click if the click is not on previous
        # revealed image or tile with user defined color,
        # and no more than 2 image revealed each round
        if 'image' not in current_tags and self.images_per_round < 2 \
                and self.canvas.itemcget(tkinter.CURRENT, 'fill') != \
                self.color:
            self.canvas.addtag_withtag('selected', tkinter.CURRENT)

            # get the coordinate of the selected tile
            x1_pos, y1_pos, x2_pos, y2_pos = self.canvas.coords(
                                                  tkinter.CURRENT)

            # Create image on the selected tile
            self.canvas.create_image((x1_pos + x2_pos) / 2,
                                     (y1_pos + y2_pos) / 2,
                                     image=self.image_dict[current_tags[0]]
                                     , tags='image')

            # Increment the number of revealed images
            self.images_per_round += 1

            # If two images have been revealed
            if self.images_per_round == 2:
                self.canvas.after(self.delay, self.hide)

    def hide(self):
        """
        This method is called after a delay to hide the two tiles that
        were flipped. The method will also change the tile color to the
        user specified color if there is a match.
        :return: None
        """
        selected_tiles = self.canvas.find_withtag('selected')

        # If two images have been revealed
        if len(selected_tiles) == 2:
            # Get the first and second selected tiles
            first_tile = selected_tiles[0]
            second_tile = selected_tiles[1]

            # Get the associated image names of
            # the first and second selected tiles
            first_image = self.canvas.gettags(first_tile)[0]
            second_image = self.canvas.gettags(second_tile)[0]

            # Fill the color if there is a match
            if first_image == second_image:
                self.canvas.itemconfigure(first_tile, fill=self.color)
                self.canvas.itemconfigure(second_tile, fill=self.color)
                self.pair_match += 1

            # Delete 'selected' tags and images
            self.canvas.dtag(first_tile, 'selected')
            self.canvas.dtag(second_tile, 'selected')
            self.canvas.delete('image')

            # reset the number of revealed images
            self.images_per_round = 0

            # Increment the number of tries
            self.tries += 1
            if self.tries > 13:
                self.score -= 10
                self.status.configure(text=f'Score: {self.score}')

            # if game is over:
            if self.pair_match == 8:
                self.status.configure(text=f'Game over!\n Score: {self.score} '
                                           f'\n Number of tries: {self.tries}')


def folder_type(folder_path):
    """
     Validate the user entered folder and return the valid path.
     :param folder_path: (string) name/path of the given folder
     :return: (string) a valid path of a folder that contains
              at least 8 images
     """
    if not os.path.isdir(folder_path):
        raise argparse.ArgumentTypeError(f"{folder_path} is not a valid"
                                         f" folder")
    else:
        image_count = 0
        for file in os.listdir(folder_path):
            filename, ext = os.path.splitext(file)
            if ext == '.gif':
                image_count += 1
        if image_count >= 8:
            return folder_path
        else:
            raise argparse.ArgumentTypeError(f"{folder_path} must contain at"
                                             f" least 8 gif images")


def get_arguments():
    """
    Parse and validate the command line arguments.
    :return: tuple containing the player color (string), the image
    folder (string) and the fast option (boolean)
    """
    pass  # take out the pass statement and enter your code
    parser = argparse.ArgumentParser()
    parser.add_argument('player_color',
                        help='What color would you like for the player?',
                        choices={'blue', 'green', 'magenta'})

    parser.add_argument('image_folder',
                        help='What folder contains the game images?',
                        type=folder_type,
                        nargs='?',
                        default="images")

    parser.add_argument('-f', '--fast',
                        help='fast or slow game?',
                        action='store_true')

    arguments = parser.parse_args()
    player_color = arguments.player_color
    image_folder = arguments.image_folder
    delay = arguments.fast
    return player_color, image_folder, delay


def main():
    # Retrieve and validate the command line arguments using argparse
    player_color, image_folder, delay = get_arguments()
    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a MatchGame object with the correct arguments
    MatchGame(root, player_color, image_folder, delay)
    # Enter the main event loop
    root.mainloop()


if __name__ == '__main__':
    main()
