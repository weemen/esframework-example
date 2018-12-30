class StartGame {

    command = "StartGame";
    data = {
        aggregate_root_id: '',
        tries: 0
    };

    constructor(aggregateRootId ='', tries=0) {
        this.data.aggregate_root_id = aggregateRootId;
        this.data.tries = tries
    }

}

export default StartGame;