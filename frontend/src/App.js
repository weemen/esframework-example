import React, { Component } from 'react';
import GameInput from './components/hangman/gameInput'
// import logo from './logo.svg';
import axios from 'axios';
import {API} from './constants/hangman'
import StartGame from './components/hangman/commands/startGame'
import GuessLetter from './components/hangman/commands/guessLetter'
import GuessWord from './components/hangman/commands/guessWord'
import uuid from 'uuidv4'
import './App.css';
import GameVisualState from "./components/hangman/gameVisualState";

class App extends Component {

  gameId = uuid();

  state = {
      triesLeft: 10,
      wordState: null,
      wrongGuessedLetters: [],
      gameState: 'ACTIVE',
  }

  componentDidMount = () => {
      console.log("Game id = "+this.gameId);
      this.startGame();
  };

  render() {
    return (
      <div className="App">
          <h1>The Hangman Game</h1>
        {/*<header className="App-header">*/}
          {/*<img src={logo} className="App-logo" alt="logo" />*/}
        {/*</header>*/}
        <div>
            <GameVisualState
                triesLeft={this.state.triesLeft}
                wordState={this.state.wordState}
                wrongGuessedLetters={this.state.wrongGuessedLetters}
            />
            <GameInput
                validateGuessLetter={this.guessLetter}
                validateGuessWord={this.guessWord}
                gameState={this.state.gameState}
            />
        </div>
      </div>
    );
  };

  startGame = () => {
      axios.post(
          API.HANGMAN_GUESS,
          JSON.stringify(new StartGame(this.gameId, 10))
      ).then(
          () => {
              this.gameStatus()
          }
      );
  };

  guessLetter = (letter) => {
      return axios.post(
          API.HANGMAN_GUESS,
          JSON.stringify(new GuessLetter(this.gameId, letter))
      ).then(
          () => {this.gameStatus()}
      ).catch(
          () => {this.gameStatus()}
      )
  };

  guessWord = (word) => {
      return axios.post(
          API.HANGMAN_GUESS,
          JSON.stringify(new GuessWord(this.gameId, word)
          )
      ).then(
          () => {this.gameStatus()}
      ).catch(
          () => {this.gameStatus()}
      )
  };

  gameStatus = () => {
      axios.get(API.HANGMAN_GAME_STATUS+'?game_id='+this.gameId).then((response) => {
          this.setState((state) => ({
              triesLeft: response.data.tries_left,
              wordState: response.data.word_state,
              wrongGuessedLetters: response.data.wrong_guessed_letters,
              gameState: response.data.game_state,
          }));
      });

  }
}

export default App;
