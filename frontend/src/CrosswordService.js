export class CrosswordService {

    constructor(setResponse) {
        this.setResponse = setResponse;
    }

    postCrossword(length, width) {
        return fetch(process.env.REACT_APP_FETCH_LINK+"crossword/?width=" + width + "&length=" + length, { //http://localhost:5000/?width="
          method: 'POST',
        }).then(res => res.json());
    }

    getTaskState(jobID) {
        return fetch(process.env.REACT_APP_FETCH_LINK+'jobs/'+jobID).then((res) => res.json());
    }

    getStatus(jobID) {
        return this.getTaskState(jobID).then((res) => {
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
                this.getStatus(res.data.job_id);
            }, 1000);
        
        })
    }
}