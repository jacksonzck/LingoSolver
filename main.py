from string import ascii_lowercase, digits
from functools import partial
from typing import Callable, List
from itertools import cycle, product, permutations
import keyboard
from time import sleep
import requests
import re

ENGLISH_DICTIONARY = None
with open("english.txt") as f:
    ENGLISH_DICTIONARY = [l.strip() for l in f.readlines()]

def brown_orange_panel_mid(input: str) -> str:
    outp = ""
    for character in input:
        index = ascii_lowercase.rfind(character)
        if index != -1:
            outp = outp + ascii_lowercase[25 - index]
    return outp

def blue_orange_panel_mid(input: str, count: int) -> str:
    outp = ""
    for character in input:
        index = ascii_lowercase.rfind(character)
        index = (index + count) % 25
        outp = outp + ascii_lowercase[index]
    return outp

def blue_orange_panel_mid_reversed(input: str) -> str:
    outp = ""
    for character in input:
        index = ascii_lowercase.rfind(character)
        if index == 0: 
            index = 25
        else:
            index -= 1
        outp = outp + ascii_lowercase[index]
    return outp

def green_numbers(input: str):
    board = \
    ["REHDCGE", "LOnSPRL", "RTAOIST", "XQEDnEH", "BIGPCIH"]
    outp = ""
    for sequence in input.split():
        if len(sequence) > 2: continue
        y = int(sequence[0]) - 1
        x = int(sequence[1]) - 1
        outp = outp + board[y][x]
    return outp

def orange(input: str, cypher:str = "wanderlust"):
    cypher = cypher[-1] + cypher[0:-1]
    outp = ""
    for character in input:
        if character not in digits: return
        outp = outp + cypher[int(character)]
        pass
    return outp

def multi_cypher_orange(input: str, cyphers: list):
    outp = ""
    for character, cypher in zip(input, cycle(cyphers)):
        outp = outp + orange(character, cypher)
    return outp

def orange_handler() -> Callable:
    while True:
        known_cyphers = [
            ("1234567890", "Reference Stem"),
            ("wanderlust", "White Stem"),
            ("theroaming", "Black Stem"),
            ("jukeboxing", "Green Stem"),
            ("fuzzy eyes", "Yellow Stem"), # ZZZ
            ("equivocate", "Red Stem"), # IIII
            ("absorption", "Blue Stem"), # Contains BB somewhere
            ("typeinover", "Over Map"),
            ("mutedchaos", "The Annex")
            # eu?ls
        ]

        print("Known cyphers are:")
        [print(f"{index}: {value[0]} ({value[1]})") for (index, value) in enumerate(known_cyphers)]
        print("Use which one?")
        try:
            return partial(multi_cypher_orange, cyphers=[known_cyphers[int(index)][0] for index in input()])
        except Exception:
            print("Invalid choice.")
        
def stop_signs():
    """
    blue = ["rip", "not", "boars", "stop", "potato"]
    black = ["merge", "tear", "roam"]
    yellow = ["-eyes", "-see", "yes", "-fee", "eyes", "fuse"],
    red = ["-voice", "aqua", "-quiet", "-activate", "taco", "-vote"],
    green = ["no", "book", "engine", "bike", "beige"],
    white = ["letter", "-start", "wander"]"""
    while True:
        colors = {
            "blue": ["rip", "not", "boars", "stop", "potato", "brain"],
            "black": ["merge", "tear", "roam"],
            "yellow": ["eyes", "see", "yes", "fee", "eyes", "fuse"],
            "red": ["voice", "aqua", "quiet", "activate", "taco", "vote"],
            "green": ["no", "book", "engine", "bike", "beige", "oxen"],
            "white": ["letter", "start", "wander"]
        }
        print("The colors are:")
        for color in colors.keys():
            print(color)
        print("What colors do you want to uss? \nColor 1:")
        color1 = input()
        print("Color 2:")
        color2 = input()
        try: 
            for word1, word2 in product(colors[color1], colors[color2]):
                print(word1 + word2)
            return
        except Exception:
            print("Invalid Colors")

def brute_force(letter_start: chr, length: int) -> list[str]:
    if letter_start != " ":
        return filter(lambda word: len(word) == length and word[0] == letter_start, ENGLISH_DICTIONARY)
    else:
        return filter(lambda word: len(word) == length, ENGLISH_DICTIONARY)

def brute_force_handler():
    while True:
        try:
            print("Starting Character:")
            starting_character = input()[0]
            print("Length")
            length = int(input())
            correct_words = brute_force(length=length, letter_start=starting_character)
            print("Going in 5 seconds!")
            sleep(5)
            for word in correct_words:
                if keyboard.is_pressed("esc"): break
                keyboard.write("the " + word)
                sleep(0.1)
            return 
        except Exception:
            print("Invalid Input")

def picasso():
    known_cyphers = [
            ("wanderlust", "White Stem"),
            ("theroaming", "Black Stem"),
            #("wanderlust", "White Stem"),
            ("fuzzy eyes", "Yellow Stem"), # ZZZ
            # Fuzzy eyes????
            ("equivocate", "Red Stem"), # IIII
            ("absorption", "Blue Stem") # Contains BB somewhere
            # eu?ls
        ]
    for permute in permutations([cypher[0] for cypher in known_cyphers], 5):
        word = multi_cypher_orange("18470", permute)
        #if word in [dicts.strip() for dicts in ENGLISH_DICTIONARY]:
        print(word)

def white_bottom(input: str):
    response = requests.get(f"https://api.datamuse.com/words?ml={input}&max=1000")
    return ";".join([rep["word"] for rep in response.json()])

def blue_bottom(input: str):
    response = requests.get(f"https://api.datamuse.com/words?rel_par={input}&max=1000")
    words = [rep["word"] for rep in response.json()]
    if input[-1] == "s":
        words.extend([rep["word"] for rep in requests.get(f"https://api.datamuse.com/words?rel_par={input[0:-1]}&max=1000").json()])
    return ";".join(words)

def black_bottom(input: str):
    response = requests.get(f"https://api.datamuse.com/words?rel_ant={input}&max=1000")
    words = [rep["word"] for rep in response.json()]
    if input[-1] == "s":
        words.extend([rep["word"] for rep in requests.get(f"https://api.datamuse.com/words?rel_ant={input[0:-1]}&max=1000").json()])
    return ";".join(words)

def bool_response() -> bool:
    try:
        return input().lower()[0] == "y"
    except Exception:
        return False

def regex_handler(word_list: List[str]) -> List[str]:
    print("Match some regex?")
    if not bool_response(): return word_list
    print("Regex you want to match:")
    regex_input = input()
    output_list = list()
    for word in word_list:
        if re.fullmatch(regex_input, word) != None:
            output_list.append(word)
    return output_list


def entire_damn_dictionary(input: str) -> List[str]:
    words = ENGLISH_DICTIONARY
    def count_characters(input: str) -> dict:
        character_counts = dict()
        for character in input:
            if character in character_counts:
                character_counts[character] = character_counts[character] + 1
            else:
                character_counts[character] = 1
        return character_counts
    return_words = list()
    input_characters = count_characters(input)
    for word in words:
        try:
            word_characters = count_characters(word)
            word_okay = True
            for character, count in input_characters.items():
                if word_characters[character] < count: word_okay = False
            if word_okay: return_words.append(word)
        except Exception:
            pass
    return ";".join(return_words)

def yellow_middle(input: str):
    words = ENGLISH_DICTIONARY
    def count_characters(input: str) -> dict:
        character_counts = dict()
        for character in input:
            if character in character_counts:
                character_counts[character] = character_counts[character] + 1
            else:
                character_counts[character] = 1
        return character_counts
    return_words = list()
    input_characters = count_characters(input)
    for word in words:
        if len(word) != len(input): continue
        try:
            word_characters = count_characters(word)
            word_okay = True
            for character, count in input_characters.items():
                if word_characters[character] == count: word_okay = False
            if word_okay: return_words.append(word)
        except Exception:
            pass
    return ";".join(return_words)
    
def code():
    sleep(5)
    for i in range(10000):
        if keyboard.is_pressed("esc"): break
        keyboard.write(str(i))
        sleep(.1)
        keyboard.write("\b\b\b\b")
        sleep(.1)
        

def main():
    func = None
    match input().lower():
        case "bo": func = brown_orange_panel_mid
        case "gn": func = green_numbers
        case "o": func = orange_handler()
        case "blo": func = partial(blue_orange_panel_mid, count=int(input()))
        case "ro": func = partial(blue_orange_panel_mid, count=-1 * int(input()))
        case "stop": return stop_signs()
        case "brute": return brute_force_handler()
        case "picasso": return picasso()
        case "wb": func = white_bottom
        case "bb": func = blue_bottom
        case "blb": func = black_bottom
        case "dd": func = entire_damn_dictionary
        case "co": return code()
        case default: return
    print("Insert word to convert:")
    outp = func(input().lower())
    words = outp.split(";")
    if len(words) == 1:
        print(outp)
    else: 
        words = regex_handler(words)
        print(f"Found {len(words)} words.")
        print("How many to show?")
        shows = 0
        try: 
            shows = int(input())
        except Exception: 
            shows = len(words)
        if shows > len(words): shows = len(words)
        print("Brute Force?")
        force_it = bool_response()
        if force_it: 
            print("5 seconds to brute force")
            sleep(5)
        for word in words[:shows]:
            if keyboard.is_pressed("esc"): break
            if force_it:
                keyboard.write(word)
                sleep(0.1)
                keyboard.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
                sleep(0.1)
            else:
                print(word)
    print("That's it!")
    print("Want to go again?")
    if input().lower()[0] == "y": main()


if __name__ == "__main__":
    main()


# Black's 890 GREEN - Black's ING?