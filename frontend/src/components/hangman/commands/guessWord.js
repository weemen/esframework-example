class GuessWord {

    command = "GuessWord";
    data = {
        aggregate_root_id: '',
        word: ''
    };

    constructor(aggregateRootId ='', word='') {
        this.data.aggregate_root_id = aggregateRootId;
        this.data.word = word;
    }

}

export default GuessWord;