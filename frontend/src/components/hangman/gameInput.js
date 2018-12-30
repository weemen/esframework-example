import React, { Component } from 'react';

class GameInput extends Component {
    state = {
        guessing_letter: '',
        guessing_word: ''
    };

    renderGameLostScreen = () => {
        return (
            <div>
                <h3>MUHAHAHAHAHA Game Over!!</h3>
                <a href={window.location.href}>Try Again</a>
            </div>
        )
    };

    renderGameWonScreen = () => {
        return (
            <div>
                <h3>Well done, this time you win!!</h3>
                <a href={window.location.href}>Try Again</a>
            </div>
        )
    };

    renderActiveGameScreen = () => {
        return (
            <div className="overallContainer">
                <div className="controlContainer">
                    <div className="itemContainerLabel">
                        <label htmlFor="letter">Guess a letter</label>
                    </div>
                    <div className="itemContainer">
                        <input type="text"
                               name="letter"
                               value={this.state.guessing_letter}
                               onChange={ field => this.setState({guessing_letter: field.target.value})}
                        />
                    </div>
                    <div className="itemContainer">
                        <button type="button"
                                onClick={ () => this.handleOnGuessLetter() }
                        >Guess letter</button>
                    </div>
                </div>
                <div className="controlContainer">
                    <div className="itemContainerLabel">
                        <label htmlFor="letter">Guess the word</label>
                    </div>
                    <div className="itemContainer">
                        <input type="text"
                               name="word"
                               value={this.state.guessing_word}
                               onChange={ field => this.setState({guessing_word: field.target.value})}
                        />
                    </div>
                    <div className="itemContainer">
                        <button type="button"
                                onClick={ () => this.handleOnGuessWord() }
                        >Guess word</button>
                    </div>
                </div>
            </div>
        );
    };

    render() {
        if (this.props.gameState === 'LOST') {
            return this.renderGameLostScreen()
        } else if  (this.props.gameState === 'WIN'){
            return this.renderGameWonScreen()
        } else {
            return this.renderActiveGameScreen()
        }
    };

    handleOnGuessLetter = () => {
        this.props.validateGuessLetter(this.state.guessing_letter)
        this.setState({guessing_letter: ''})
    };

    handleOnGuessWord = () => {
        this.props.validateGuessWord(this.state.guessing_word)
        this.setState({guessing_word: ''})
    };
}

export default GameInput;