#tic-tac-toe
#well well well, 6 years later and im still making shitty tic tac toe games lol.

"""
8/18/24 ~ 
    gotta start somewhere, so ig we will start with writing a bunch of Pseudo
    i dont have it in me to write any boilerplate for everything thats needed to
    even do any of this so im just gonna write the structure of how the game 
    will work, thats the best i can do.

    ideally id like to shove all the screen handling and user input handling in
    to separate files corresponding to what system you are using. linux, unix or
    windows system.

    the reasoning behind this is id like to at least to a modicum make the game
    replayable and somewhat fun so im gonna be adding different versions of-
    -tic tac toe to the game

    so far the first version will just be the basic tictactoe everyone knows and
    loves but also hates, its gonna have a varying degree of difficulty but only
    on a scale from 1-3, 1 being brain dead random and 3 being a scratch every
    game as tictactoe is stupidly simple and a weakly solved game using minimax

    my next decision might be to make a "Chaos" version where everything is bat
    shit crazy and the board throws random rules at you from various and even-
    -sometimes completely random events hardcoded into the game itself

        ~Dylan

8/24/24 ~
    THE NAME OF THE GAME chaos tic tac toe
    this will be a little more than just chaos tic tac toe though. my own-
    -version of it, being three different modes of game play as described below.

        ~ MODE ONE ~
            A basic game of tic-tac-toe will be played in version one, prefer-
            -ably with some basic colored console output and crude visuals

            nothing fancy going on here except for the games difference in
            difficulty still being the same as described before ranking 1 to 3,
            
            1 to 3 will only describe the algorithm used to solve the game and
            thats really it.

        ~ MODE TWO ~
            My own version of tic tac toe called Chaos Tic Tac Toe, where the 
            players play on three boards simultaneously. the player to get all
            three boards, or the greatest amount of boards won, wins.

            the rules of this game are still a bit fuzzy but all in all a 
            scratch doesn't result in a endgame tie but a type of "Overtime"
            with the players being forced to make moves quickly under a time
            limit, if a player exceeds this time limit a move is made at random

        ~ MODE THREE ~
            Pandemonium tic-tac-toe, the ultimate version of chaos, instead of 
            just three boards the players play on nine boards arranged in a 3x3
            square, same rules as basic tic tac toe but you must win a board to
            win a square, the game is also altered to become more chaotic. 
            
            ~ Square Scratch ~
                in the event the player or comp scratches on a square every
                available square will have its contents randomly rearranged,
                this should make the playability of the game longer and more
                interesting as it removes the tie condition from the game
                and instead makes the players more conscious about just making
                the board scratch on the computer.

                No shuffle of any board will result in the board being won or
                lost by the player of computer and in the event its required a 
                space be open,  a players move may be removed, but only the last
                played move on that square.

            ~ Win Condition ~
                to win Pandemonium you must get three squares in a row, meaning
                win three boards in a basic tic tac toe configuration to win the
                game... simple right?

            ~ OverTime Condition ~
                in the event the player scratches on the board and there is no
                available square to play out a sudden death. the game goes
                into a state of overtime. similar to chaos the players must
                select there moves not under a time constraint. with each open
                space of each board taken removing more and more time available
                to make a move.

                Furthermore, in overtime. the game does not accept a scratch
                from the board. or squares simultaneously now instead of a
                sudden death. the board and its subsequent squares are all
                shuffled randomly. with the last move to be made removed.

                same rules as pandemonium, win three squares to win the game.
 
        ~ CUSTOM GAME MODES ~

            Custom game modes is something id like to add as a more "endgame"
            game mode for players to play if they get board of having to play
            the same game modes over and over. While one can change the symbols
            and colors of the game at will within the games settings at any time
            this will change how the game functions without effecting game rules

            players will be able to select between board size and wether or not
            they would like to play against another player on the same computer.

            this is a basic change to the functionality of basic tic-tac-toe
            but is a nice implementation of a player conditioned game where it 
            should result in even more re-playability of the game over time.

    this game will be fun i think. maybe it wont be. but its a start to
    something i feel like is very very interesting to watch or build...

    the reason im making this game and making these choices is because i know
    the extent of my knowledge of programming and algorithms, my hope is that
    by building this game and building it within the scope ive given myself
    it will make me a better software developer. while i have never fully
    written any software that works or stays working im confident in making
    something out of this idea, im confident my skills as a programmer over the 
    past 8 years (albeit only 4 years of actual coding) will be enough to make
    something as simple (or maybe as complex) as this rendition or varient of
    tic-tac-toe
        ~Dylan
"""

from screen import *
from option import *
from tictactoe import TicTacToe, ChaosTtt, PandemoniumTtt
import os, time

class Game:

    def __init__(self):
        #game constants here
        self.screen = Screen()
        self.input = Inputs()
        self.inp_handle = self.input.handle
        self.baseTtt = TicTacToe(self)
        self.chaosTtt = ChaosTtt(self)
        self.pandeTtt = PandemoniumTtt(self)

    def GameLoop(self):
        self.inp_handle.clear_bindings()
        options = OptionGroup([{
                "key": 't',
                "name": "TicTacToe",
                "action": self.baseTtt.GameLoop
            },
            {
                "key": 'c',
                "name": "Chaos TicTacToe",
                "action": self.chaosTtt.GameLoop
            },
            {
                "key": 'p',
                "name": "Pandemonium TicTacToe",
                "action": self.pandeTtt.GameLoop
            },
            {
                "key": 'q',
                "name": "Quit",
                "action": self.Quit
            }
        ])
        self.screen.clear()
        self.screen.menu(options)
        self.inp_handle.bind_options(options)
        while True:
            self.inp_handle.listener()

    def MainMenu(self):
        #static variables and definitions go here
        self.inp_handle.clear_bindings()
        options = OptionGroup([{
                "key": 'p',
                "name": "Play",
                "action": self.Play
            },
            {
                "key": 'q',
                "name": "Quit",
                "action": self.Quit
            }
        ])
        self.screen.clear()
        self.screen.menu(options)
        self.inp_handle.bind_options(options)
        print(self.input.awaiting())
        while True:
            self.inp_handle.listener()
            
    def Play(self):
        self.screen.clear()
        self.screen.printAtCenter("Ready for some Tic Tac Toe?")
        time.sleep(5)
        self.GameLoop()

    def Quit(self):
        self.screen.clear()
        self.screen.printAtCenter(
            "thank you for using my software!"
        )
        time.sleep(5)
        os._exit(0)

if __name__ == "__main__":
    game = Game()
    game.MainMenu()

