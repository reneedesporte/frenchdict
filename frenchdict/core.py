"""Main module for the `frenchdict` application."""

import sys
import os
import json
from utils import commands

FR_EN_DICT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pared__kaikki.org-dictionary-French.json")  # TODO fix path once package is installable

def introduction():
    """Print introduction message to application.
    
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    print(
        "\n..........................................................\n"
        "...#######.####...........####..........######.###...##...\n"
        "...##......##..##........##...##........##.....####..##...\n"
        "...######..####.....##.......##....##...#####..##.##.##...\n"
        "...##......##.##...........##...........##.....##..####...\n"
        "...##......##..##.........######........######.##...###...\n"
        "..........................................................\n"
    )
    print("A CLI for doing French-to-English and English-to-French translations.")
    print("DISCLAIMER: The dictionary used for this application contains profanities.")
    print("For more information, "
          "please see the repo at https://github.com/reneedesporte/frenchdict.\n")

    print("Options:")
    for key, val in commands.items():
        print(f"     {val}: {key}")
    print("\n")

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
        print(f"Couldn't find the dictionary file at '{path_to_dict}'.\n")
        sys.exit(0)

    return fr_to_en

def calculate_english_to_french_dict(fr_to_en):
    """Calculate the English to French dictionary from the saved French-to-English one.
    
    Parameters
    ----------
    fr_to_en : dict
        Dictionary containing the French words as keys.
    
    Returns
    -------
    dict
        Dictionary containing English words as keys.
    """
    en_to_fr = {}
    for key, values in fr_to_en.items():
        for value in values:
            if value not in en_to_fr:
                en_to_fr[value] = [key]
                continue
            en_to_fr[value].append(key)

    return en_to_fr

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
    help_msg = ("\nType any word in English to get its French translation.\n"
                "Other options:\n    'q' to go back to the main menu.\n    "
                "'h' or 'help' for this message.\n")
    print(help_msg)
    while True:
        word = input("[English-to-French]: ")
        if word == "h":
            print(help_msg)
            continue
        if word == "q":
            if yes_or_no("Are you sure you want to go back to the main menu? [Y/n]: "):
                return
        if word in dictionary.keys():
            base = f"The French translation of '{word}' is \n"
            for w in dictionary[word]:
                base = f"{base}    - {w}\n"
            print(base)
            continue
        print(f"Couldn't find the English word '{word}' in our dictionary.")

def get_english_translation(dictionary):
    """Get user input in French and translate to English.
    
    Parameters
    ----------
    dictionary : dict
        Dictionary with French words as keys.
    """
    help_msg = ("\nType any word in French to get its English translation.\n"
                "Other options:\n    'q' to go back to the main menu.\n    "
                "'h' or 'help' for this message.\n")
    print(help_msg)
    while True:
        word = input("[French-to-English]: ")
        if word == "h":
            print(help_msg)
            continue
        if word == "q":
            if yes_or_no("Are you sure you want to go back to the main menu? [Y/n]: "):
                return
        if word in dictionary.keys():
            base = f"The English translation of '{word}' is \n"
            for w in dictionary[word]:
                base = f"{base}    - {w}\n"
            print(base)
            continue
        print(f"Couldn't find the French word '{word}' in our dictionary.")

def command_line_parser(valid_commands, loaded_french_dict, en_to_fr_dict):
    """Get user input for non-translation tasks, e.g., "help".
    
    Parameters
    ----------
    valid_commands : list of str
        List of allowable commands.
    loaded_french_dict : dict
        Fr-to-En dictionary loaded from json.
    en_to_fr_dict : dict
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
        get_french_translation(en_to_fr_dict)
    elif command in ("english", "e"):
        get_english_translation(loaded_french_dict)
    elif command in ("quit", "q"):
        print("\nExiting...")
        sys.exit(0)

def main():
    """Main function within command-line interactions occur."""
    introduction()
    allowable_commands = [
        c
        for c_list in commands.values()
        for c in c_list
    ]

    loaded_dict = load_in_dictionary(FR_EN_DICT)
    calculated_dict = calculate_english_to_french_dict(loaded_dict)

    try:
        while True:
            command_line_parser(allowable_commands, loaded_dict, calculated_dict)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
