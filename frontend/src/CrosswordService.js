export class CrosswordService {

    constructor(setResponse) {
        this.setResponse = setResponse;
    }

    postCrossword(length, width) {
        return fetch("http://localhost:5000/?width="+ width + "&length=" + length, {
          method: 'POST',
        }).then(res => res.json());
    }

    getTaskState(jobID) {
        return fetch('http://localhost:5000/jobs/'+jobID).then((res) => res.json());
    }

    getStatus(jobID) {
        return this.getTaskState(jobID).then((res) => {
            let jobStatus = res.data.job_status;
            console.log(jobStatus);
            if (jobStatus === 'finished'){
                this.setResponse(res);
                return res;
            }
            else if (jobStatus === 'failed') return false;
        
            setTimeout(() => {
                this.getStatus(res.data.job_id);
            }, 1000);
        
        })
    }
}