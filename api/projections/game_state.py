from esframework.event_handling.event_listener import EventListener

from api.domain.events import LetterGuessed, GameStarted, LetterNotGuessed, GameWon, GameLost, WordGuessed
from api.projections.game_state_model import GameStateModel


class GameStateProjection(EventListener):

    def __init__(self, session):
        self.__session = session

    def apply_game_started(self, domain_event: GameStarted):
        projection = GameStateModel(
            aggregate_root_id=domain_event.get_aggregate_root_id(),
            tries_left=domain_event.get_tries(),
            word=domain_event.get_word(),
            word_state='*' * len(domain_event.get_word()),
            wrong_guessed_letters=[],
            game_state='ACTIVE'
        )

        self.__session.add(projection)
        self.__session.commit()

    def apply_letter_guessed(self, domain_event: LetterGuessed):
        record = self.__session.query(GameStateModel) \
            .filter_by(aggregate_root_id=domain_event.get_aggregate_root_id()) \
            .one()

        if not record:
            raise RuntimeError(
                'Aggregate root id does not exist',
                domain_event.get_aggregate_root_id())

        replace_list = [pos for pos, char in enumerate(record.word) if char == domain_event.get_letter()]
        word = list(record.word_state)
        for pos in replace_list:
            word[pos] = domain_event.get_letter()
        record.word_state = ''.join(word)
        self.__session.commit()

    def apply_letter_not_guessed(self, domain_event: LetterNotGuessed):
        record = self.__session.query(GameStateModel) \
            .filter_by(aggregate_root_id=domain_event.get_aggregate_root_id()) \
            .one()

        if not record:
            raise RuntimeError(
                'Aggregate root id does not exist',
                domain_event.get_aggregate_root_id())

        record.tries_left -= 1
        record.wrong_guessed_letters.append(domain_event.get_letter())

        self.__session.commit()

    def apply_word_guessed(self, domain_event: WordGuessed):
        record = self.__session.query(GameStateModel) \
            .filter_by(aggregate_root_id=domain_event.get_aggregate_root_id()) \
            .one()

        if not record:
            raise RuntimeError(
                'Aggregate root id does not exist',
                domain_event.get_aggregate_root_id())

        record.wrong_guessed_word = domain_event.get_word()
        self.__session.commit()

    def apply_game_won(self, domain_event: GameWon):
        record = self.__session.query(GameStateModel) \
            .filter_by(aggregate_root_id=domain_event.get_aggregate_root_id()) \
            .one()

        if not record:
            raise RuntimeError(
                'Aggregate root id does not exist',
                domain_event.get_aggregate_root_id())
        record.game_state = 'WIN'
        self.__session.commit()

    def apply_game_lost(self, domain_event: GameLost):
        record = self.__session.query(GameStateModel) \
            .filter_by(aggregate_root_id=domain_event.get_aggregate_root_id()) \
            .one()

        if not record:
            raise RuntimeError(
                'Aggregate root id does not exist',
                domain_event.get_aggregate_root_id())
        record.game_state = 'LOST'
        self.__session.commit()
