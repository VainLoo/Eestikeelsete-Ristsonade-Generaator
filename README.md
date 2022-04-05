# Eestikeelsete-Ristsonade-Generaator
Bakalaureusetöö eesmärk oli luua eestikeelsete ristsõnade generaator, mis kasutab eesti keele keeleressursse (analüsaatorid, süntesaatorid, sõnastikud jne) ja kogub muu vajaliku info veebist. Tulemuseks saadud ristsõna oli nii paberile trükitav kui ka lahendatav ja kont-rollitav otse veebilehel. Genereerimisel kasutatavad andmed koguti eestikeelsest Vikipee-diast kasutades veebisorimist (web crawling), Eesti Wordnetist kasutades selles olevad definitsioone ja EstNLTK morfoloogilist sünteesi. Ristsõna genereeriti kasutades kitsen-duste rahuldamise meetodit. Töös kirjeldatakse andmete kogumise metoodikat, ristsõna genereerimist ja lõpplikku veebirakendust ennast. 

## Dockeriga jooksutamine 
```
$ docker-compose up -d --build
```

Veebirakendus jookseb aadressil: http://localhost/
