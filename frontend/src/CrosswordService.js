export class CrosswordService {

    constructor(setResponse) {
        this.setResponse = setResponse;
    }

    postCrossword() {
        return fetch(process.env.REACT_APP_FETCH_LINK+"crossword/", { 
          method: 'POST',
        }).then(res => res.json());
    }

    getTaskState() {
        return fetch(process.env.REACT_APP_FETCH_LINK+'jobs/').then((res) => res.json());
    }

    getStatus() {
        return this.postCrossword().then((res) => {
            let jobStatus = res.data.job_status;
            console.log(jobStatus);
            if (jobStatus === 'finished'){
                this.setResponse(res);
                return res;
            }
            else if (jobStatus === 'failed') {
                this.setResponse(jobStatus);
                return false;
            }
            setTimeout(() => {
                this.getStatus();
            }, 1000);
        
        })
    }
}