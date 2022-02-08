export class CrosswordService {

    getCrossword() {
        return fetch("http://127.0.0.1:5000/")
        .then(res => res.json());
    }
}