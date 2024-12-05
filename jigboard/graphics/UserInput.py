from typing import Callable

# UserInput class to store user input then run the function in the update loop
# prevents the user input events from crashing the program
class UserInput:
    run : bool = False
    # this is any function that takes no arguments
    function : Callable