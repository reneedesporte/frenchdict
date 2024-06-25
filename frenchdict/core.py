"""Main module for the `frenchdict` application."""

import sys
import os
import json
from utils import commands

FR_EN_DICT = os.path.join("docs", "pared__kaikki.org-dictionary-French.json")  # TODO fix path once package is installable

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

def load_in_dictionary(path_to_dict):
    """Load in the French-to-English dictionary.
    
    Parameters
    ----------
    path_to_dict : pathlike
        Path to json file containing French-to-English translations.
    
    Returns
    -------
    dict
        Dictionary containing French words as keys.
    TODO : implement English-words-as-keys dict.
    """
    try:
        with open(path_to_dict, "r", encoding="utf8") as f:
            lines = [line.rstrip() for line in f]
            fr_to_en = json.loads(lines[0])
    except FileNotFoundError:
        print(f"Couldn't find the dictionary file at '{path_to_dict}'.\n"
              "Please run the program from the top-most level of the repo.")
        sys.exit(0)

    return fr_to_en

def get_french_translation(dictionary):
    """Get user input in English and translate to French.
    
    Parameters
    ----------
    dictionary : dict
        Dictionary with English words as keys.

    Returns
    -------
    None
    """
    while True:
        word = input("Type any word in English to get its French translation: ")
        if word in dictionary.keys():
            translated_word = dictionary[word]
            print(f"The translation of '{word}' is '{translated_word}'.")
            continue
        if not yes_or_no(f"Couldn't find '{word}' in our dictionary."
                            " Try another word? [Y/n]: "):
            return

def get_english_translation(dictionary):
    """Get user input in French and translate to English.
    
    Parameters
    ----------
    dictionary : dict
        Dictionary with French words as keys.
    """
    help_msg = print("\nType any word in French to get its English translation, or 'q' to go back to the main menu.")
    while True:
        word = input("[French-to-English]: ")
        if word == "q":
            if yes_or_no("Are you sure you want to go back to the main menu? [Y/n]: "):
                return
        if word in dictionary.keys():
            translated_word = dictionary[word]
            print(f"The translation of '{word}' is '{translated_word}'.")
            continue
        print(f"Couldn't find the French word '{word}' in our dictionary.")

def command_line_parser(valid_commands, loaded_french_dict, en_to_fr_dict=None):
    """Get user input for non-translation tasks, e.g., "help".
    
    Parameters
    ----------
    valid_commands : list of str
        List of allowable commands.
    loaded_french_dict : dict
        Fr-to-En dictionary loaded from json.
    en_to_fr_dict : dict, default=None
        En-to-Fr dictionary loaded from json.
    """
    command = input("[frenchdict]: ")
    if command not in valid_commands:
        print(f"Bad command: '{command}'! Options:")
        for key, val in commands.items():
            print(f"     {val}: {key}")
    elif command in ("help", "h"):
        for key, val in commands.items():
            print(f"     {val}: {key}")
    elif command in ("french", "f"):
        print("The English-to-French translation is not yet implemented.")
        # get_french_translation(en_to_fr_dict)
    elif command in ("english", "e"):
        get_english_translation(loaded_french_dict)
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

    loaded_dict = load_in_dictionary(FR_EN_DICT)
    print(f"Loaded dictionary with {len(loaded_dict.keys())} French words.")

    try:
        while True:
            command_line_parser(allowable_commands, loaded_dict)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
