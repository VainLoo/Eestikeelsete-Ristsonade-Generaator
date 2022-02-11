export class CrosswordService {

    getCrossword() {
        return fetch("http://localhost:8080/")
        .then(res => res.json());
    }
}