import React, { Component } from 'react';

class GameVisualState extends Component {

    render() {
        const image = require(`../../assets/img/${this.props.triesLeft}.png`);
        const wrongGuesses = this.props.wrongGuessedLetters.join(', ');

        return (
            <div >
                <img width="500" src={image} alt={this.props.triesLeft} />
                <div className="wordstateTitle">Guess the word</div>
                <div className="wordstate">{ this.props.wordState }</div>
                <div>
                    <div className="wrongGuessesTitle">Wrong Guesses:</div>
                    <div className="wrongGuesses">
                        { wrongGuesses }
                    </div>
                </div>
            </div>
        );
    }
}

export default GameVisualState;