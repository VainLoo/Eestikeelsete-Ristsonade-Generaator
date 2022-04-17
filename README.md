# Eestikeelsete-Ristsonade-Generaator
Bakalaureusetöö eesmärk oli luua eestikeelsete ristsõnade generaator, mis kasutab eesti keele keeleressursse ja kogub muu vajaliku info veebist. Tulemuseks saadud ristsõna on nii paberile trükitav kui ka lahendatav ja kontrollitav otse veebilehel. Genereerimisel kasutata-vad andmed koguti eestikeelsest Vikipeediast kasutades veebisorimist (web crawling), Eesti Wordnetist kasutades selles olevad definitsioone ja EstNLTK morfoloogilist süntee-si. Ristsõna genereeriti, kasutades kitsenduste rahuldamise meetodit. Töös kirjeldatakse andmete kogumise metoodikat, ristsõna genereerimist ja lõplikku veebirakendust ennast. 

## Dockeriga jooksutamine 
```
$ docker-compose up -d --build
```

Veebirakendus jookseb aadressil: http://localhost/
