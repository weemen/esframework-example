from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()


class GameStateModel(Base):
    __tablename__ = 'hangman_game_state'

    aggregate_root_id = Column(String(length=36), primary_key=True)
    tries_left = Column(Integer, nullable=False)
    word = Column(String(length=255), nullable=False)
    word_state = Column(String(length=255), nullable=False)
    wrong_guessed_letters = Column(MutableList.as_mutable(JSON), nullable=False)
    wrong_guessed_word = Column(String(length=255), nullable=True)
    game_state = Column(String(length=12))

    def __repr__(self):
        return "<GameStateModel(" \
               "aggregate_root_id='%s', " \
               "tries_left='%s'" \
               "word='%s'" \
               "word_state='%s'" \
               "wrong_guessed_letters='%s'" \
               "wrong_guessed_word='%s'" \
               "game_state='%s'" \
               ")>" % \
               (self.aggregate_root_id, self.tries_left,
                self.word, self.word_state, self.wrong_guessed_letters,
                self.wrong_guessed_word, self.game_state)
