import json
import random
from api.exceptions import CommandException


class StartGame(object):
    """ StartGameCommand """

    __aggregate_root_id = None
    __word = ""
    __tries = 0

    def __init__(self, aggregate_root_id, tries: int):
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise CommandException(
                "Cannot construct command: aggregate_root_id is missing!")

        if not tries or not isinstance(tries, int):
            raise CommandException(
                "Cannot construct command: tries is missing!")

        with open("./api/assets/dictionary.json") as f:
            word_dictionary = json.load(f)

        self.__aggregate_root_id = aggregate_root_id
        self.__word = random.choice(list(word_dictionary))
        self.__tries = tries

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id

    def get_word(self):
        return self.__word

    def get_tries(self):
        return self.__tries


class GuessLetter(object):
    """ GuessLetterCommand """

    __aggregate_root_id = None
    __letter = ""

    def __init__(self, aggregate_root_id, letter: str):
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise CommandException(
                "Cannot construct command: aggregate_root_id is missing!")

        if not letter or not isinstance(letter, str) or len(letter) > 1:
            raise CommandException(
                "Cannot construct command: letter is missing!")

        self.__aggregate_root_id = aggregate_root_id
        self.__letter = letter

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id

    def get_letter(self):
        return self.__letter


class GuessWord(object):
    """ GuessWordCommand """

    __aggregate_root_id = None
    __word = ""

    def __init__(self, aggregate_root_id, word: str):
        if not aggregate_root_id or not isinstance(aggregate_root_id, str):
            raise CommandException(
                "Cannot construct command: aggregate_root_id is missing!")

        if not word or not isinstance(word, str):
            raise CommandException(
                "Cannot construct command: word is missing!")

        self.__aggregate_root_id = aggregate_root_id
        self.__word = word

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id

    def get_word(self):
        return self.__word
