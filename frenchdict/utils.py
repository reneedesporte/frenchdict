"""Module containing utilities for the `frenchdict` application."""

import json

commands = {"Print the list of allowable commands.": ["help", "h"],
            "Translate a word from English to French.": ["french", "f"], 
            "Translate a word from French to English.": ["english", "e"], 
            "Quit the application.": ["quit", "q"]}

def pare_kaikki_data(path):
    """Load in and pare down the json data from [source]
    (https://kaikki.org/dictionary/French/kaikki.org-dictionary-French.json).

    Overwrite the original Kaikki json file with the newly pared one.
    
    Parameters
    ----------
    path : pathlike
        Path to source data file.
    
    Returns
    -------
    None
    """
    with open(path, "r", encoding="utf8") as f:
        old_data = [json.loads(line.rstrip()) for line in f]

    new_dictionary = {}
    for line in old_data:
        new_dictionary[line["word"]] = []
        for sense in line["senses"]:
            if "links" not in sense.keys():
                continue
            for word in sense["links"]:
                links = word[-1].split("#")
                if links[-1] != "French":
                    new_dictionary[line["word"]].append(word[0])
        if len(new_dictionary[line["word"]]) == 0:
            new_dictionary.pop(line["word"], None)

    with open(path, "w", encoding="utf8") as f:
        json.dump(new_dictionary, f)
