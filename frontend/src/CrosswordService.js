export class CrosswordService {

    getCrossword(length, width) {
        return fetch("http://localhost:5000/?width="+width+"&length="+length)
        .then(res => res.json());
    }
}