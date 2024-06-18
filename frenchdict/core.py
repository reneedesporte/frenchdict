"""Main module for the `frenchdict` application."""

import sys
from utils import commands

def yes_or_no(message):
    """Get yes or no reply from user for input message `message`.
    
    Parameters
    ----------
    message : string
        Input message to which user should reply "Y" or "n".

    Returns
    -------
    Bool
        True if user answered yes; else, False.
    """
    while True:
        cont = input(message)
        if cont == "Y":
            return True
        if cont == "n":
            return False
        print('Type "Y" or "n".')

def get_french_translation():
    """Get user input in English and translate to French.
    
    Parameters
    ----------
    None

    Returns
    -------
    string
        The user inputted word in English.
    string
        The French translation of the user-inputted word.
    """
    while True:
        word = input("Type any word in English to get its French translation: ")
        # TODO check that `word` exists in the Fr-En dictionary
        translated_word = "VOID"
        if translated_word is not None:
            break
        if not yes_or_no(f"The word '{word}' has no French translation."
                            " Try another word? [Y/n]: "):
            return word, "N/A"
    return word, translated_word

def command_line_parser(valid_commands):
    """Get user input for non-translation tasks, e.g., "help".
    
    Parameters
    ----------
    valid_commands : list of str
        List of allowable commands.
    """
    command = input("[frenchdict]: ")
    if command not in valid_commands:
        print("Bad command! Options:")
        for key, val in commands.items():
            print(f"     {val}: {key}")
    elif command in ("help", "h"):
        for key, val in commands.items():
            print(f"     {key}: {val}")
    elif command in ("french", "f"):
        inputted_word, translation = get_french_translation()
        print(f"The translation of '{inputted_word}' is '{translation}'.")
    elif command in ("english", "e"):
        print("The French-to-English translation is not yet implemented.")
    elif command in ("quit", "q"):
        print("\nExiting...")
        sys.exit(0)

def main():
    """Main function within command-line interactions occur."""
    allowable_commands = [
        c
        for c_list in commands.values()
        for c in c_list
    ]

    try:
        while True:
            command_line_parser(allowable_commands)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
