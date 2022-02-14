export class CrosswordService {

    getCrossword(length, width) {
        return fetch("http://localhost:8080/?width="+width+"&length="+length)
        .then(res => res.json());
    }
}