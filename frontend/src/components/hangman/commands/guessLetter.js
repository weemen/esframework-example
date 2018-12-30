class GuessLetter {

    command = "GuessLetter";
    data = {
        aggregate_root_id: '',
        letter: ''
    };

    constructor(aggregateRootId ='', letter='') {
        this.data.aggregate_root_id = aggregateRootId;
        this.data.letter = letter;
    }

}

export default GuessLetter;