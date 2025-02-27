'''
You are a hero in a dark system of caves full of trolls.
You have to find a magic spell book to destroy the caves and escape.
The game will involve an engine that runs a map full of rooms or scenes.
Each room will print its own description when the player enters it and
then tell the engine what room to run next out of the map.
'''

from random import randint #we only need the random integer function not the whole module
from sys import exit #we only need the exit function for quitting the game

class Hero():
    def __init__(self):
        self.book = None
        self.coins = 0

class Engine():
    def __init__(self, scene_map):
        self.scene_map = scene_map
        # gets the game's map from instance "mymap," at bottom of this file
    def play(self):
        current_scene = self.scene_map.opening_scene()
        # see the Map object: this runs function named opening_scene()
        # this runs only once
        # this STARTS THE GAME

        while True:  # infinite loop to run the game - repeats until exit()
            print("\n--------")
            current_scene.enter()  # from Scene

            # note: will throw error if no new scene passed in by next line:
            next_scene_name = current_scene.action()

            # get the name of the next scene from the action() function that
            # runs in the current scene - what it returns

            current_scene = self.scene_map.next_scene(next_scene_name)
            #  here we use that val returned by current scene to go to
            #  the next scene, running function in Map

class Book(object):
    def __init__(self):
        self.activated = False

class Scene():
    name = 'unnamed scene'
    descrip = 'undescribed scene'

    def enter(self):
        print(self.name)
        print(self.descrip)

class GameOver(Scene):
    name = "You have died!"
    descrip = '''    You tried your best but did not succeed.\n'''

    def action(self):
        try:
            exit()  # exit the program
        except SystemExit:
            print("Game over.")

class CentralCorridor(Scene):
    '''
    A Troll is already standing here. Must be defeated
    before continuing.
    '''

    def __init__(self):
        self.troll = Troll()
        # initialize the corridor scene with a troll present

    name = "Central Corridor"
    descrip = '''    A broad passage extends in front of and behind you.
        There are doors to your left and right. There is a ladder going up.'''

    def action(self):
        if self.troll.present:
            print("    A troll is here.")
            self.troll.present, location = self.troll.fight(self.troll.stamina, self.troll.present)
            # catch the returns from fight() in Troll -
            # pass in stamina and present, get out present and current scene name
            return location
        else:
             while True:
                response = input("").lower()
                if "look" in response:
                    print(self.descrip)
                #elif "up" in response:     # uncomment when implementing the Bridge scene
                #    return 'bridge'
                elif "right" in response:
                    return 'library'
                #elif "left" in response:   # uncomment when implementing the Cave scene
                #    return 'cave'
                elif "leave" in response or "exit" in response:
                    try:
                        exit()
                    except SystemExit:
                        print("Goodbye.")
                elif response != "":
                    print("Huh? I didn't understand that.")
                else:
                    print("Something went wrong ...")
                    return 'death'

class SpellBookLibrary(Scene):
    '''
    This is where the wizard gets a magic spell book to blow up the caves before
    getting to the escape route. It has a keypad you have to guess the number for.
    '''

    def __init__(self):
        self.doorlocked = True
        self.keycode = randint(1, 9) * 111  # 3 of the same number
        self.book = Book()
        # initialize the library scene with door locked and book here

    name = "SpellBook Library"
    descrip = '''    The door to this room is closed and locked.
    There is a digital keypad set into the wall.'''
    descrip2 = '''    Shelves and cases line the walls of this room.
    Spellbooks of every description fill the shelves and cases. '''

    def action(self):
        if self.doorlocked == True:
            self.keypad()
        while True:
            response = input(">").lower()
            if "look" in response:
                print(self.descrip)
            elif "book" in response and self.book:
                print("Searching the shelves, you discover a small red case.")
                print('On the case is a label: "Explodey Spell."')
                self.take_book()
            elif "book" in response and hero.book:
                print("You are carrying the book.")
            elif "leave" in response or "exit" in response:
                return 'corridor'
            elif response != "":
                print("Huh? I didn't understand that.")
            else:
                print("Something went wrong ...")
                return 'death'

    def take_book(self):
        while True:
            response = input(">").lower()
            if "case" in response or "open" in response:
                print("You open the case and look inside. Yep. It's a book!")
                print("You close the case. It has a convenient handle for carrying.")
            elif "take" in response or "pick up" in response:
                print("You pick up the case by its handle. It is not too heavy.")
                hero.book = self.book  # now book is being carried
                self.book = None  # and the book is no longer in the library
                return
            elif "activate" in response or "set" in response:
                print("I don't think you want to do that yet.")
            elif "book" in response:
                print("Do you want to do something with the book?")
            else:
                print("Huh? What?")

    # this should probably not be infinite - should have range instead
    # it does not let you out till you get it right
    def keypad(self):
        while self.doorlocked == True:
            print("The keypad has 9 buttons with numbers from 1 to 9.")
            print("3 numbers must be entered to unlock the door.")
            response = input(">").lower()
            if "leave" in response or "exit" in response:
                return 'corridor'
            elif not response.isdigit() or (int(response)> 999 or int(response) < 100):
                print("That is not a suitable number. Try again.")
            elif int(response) == self.keycode:
                self.doorlocked = False
                print("The door slides smoothly and quietly open.")
                self.descrip = self.descrip2  # switches the description text
                print(self.descrip)
            elif int(response)> self.keycode:
                print("That number is too high.")
            elif int(response) < self.keycode:
                print("That number is too low.")
            else:
                "No good. Try again with 3 numbers."

class Troll():
    def __init__(self):
        self.present = True
        self.stamina = 10

    def report(self, s):
        if s> 8:
            print("The troll is strong! It resists your pathetic attack!")
        elif s> 5:
            print("With a loud grunt, the troll stands firm.")
        elif s> 3:
            print("Your attack seems to be having an effect! The troll stumbles!")
        elif s> 0:
            print("The troll is certain to fall soon!")
        else:
            print("That's it! The troll is finished!")
            coindrop = randint(4, 10) # Generates a random integer between 1 and 10 (inclusive)
            hero.coins = hero.coins + coindrop
            print("The Troll has dropped some coins, you now have " + str(hero.coins) + " coins!")

    def fight(self, stam, p):  # stamina and present
        while p == True:
            response = input(">").lower()
            # fight scene
            if "hit" in response or "attack" in response:
                less = randint(0, stam)
                stam -= less  # subtract random int from stamina
                self.report(stam)  # see above
                if stam <= 0:
                    p = False
                    return p, 'corridor'
                    # you end up back in corridor even if fight is on bridge
                else:
                    pass
            elif "fight" in response:
                print("Fight how? You have no weapons, silly hero!")
            else:
                print("The troll hits you with its powerful stick!")
                return p, 'death'  # new, lowered stamina number

class Map():
    scenes = {
        'death'   : GameOver(),
        'corridor': CentralCorridor(),
        'library' : SpellBookLibrary()
    }

    def __init__(self, start_scene_key):
        self.start_scene_key = start_scene_key
        # above we make a local var named start_scene_key
        # this is a string, same as the arg we passed in ('corridor')
        # start_scene_key remains unchanged throughout the game

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        # above is how we get value out of the dictionary named scenes
        return val
        # this function can be called repeatedly in the game,
        # unlike opening_scene, which is called only ONCE

    def opening_scene(self):
        return self.next_scene(self.start_scene_key)
        # this function exists only for starting, using the first
        # string we passed in ('corridor')
        # it combines the previous 2 functions and is called only once
        # (called in Engine)

hero = Hero()
mymap = Map('corridor')  # instantiate a new Map object
mygame = Engine(mymap)  # instantiate a new Engine object
mygame.play()  # call function from that Engine instance