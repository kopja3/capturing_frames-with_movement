# capturing_frames-with_movement

## Holistinen käyttöohje

Tämä projekti on lintujen tai muun liikkeen havaitsemiseen tarkoitettu järjestelmä, jossa selainkäyttöliittymä ja Python-backend toimivat yhdessä.

Järjestelmän käyttö perustuu kahteen pääosaan:

1. **Python-backend**, joka analysoi videota tai yksittäisiä frameja
2. **Selainkäyttöliittymä**, jolla käyttäjä testaa yhteyden, lataa videon, käyttää webkameraa ja tarkastelee tuloksia

Selainkäyttöliittymä löytyy tiedostosta `docs/index.html`.

---

## 1. Mitä järjestelmä tekee

Järjestelmän tarkoitus on tunnistaa videokuvasta tai kamerasyötteestä kiinnostavia kohteita ja näyttää niiden sijainti käyttäjälle visuaalisesti.

Käyttöliittymä tukee kahta päätapaa:

- **ladatun videotiedoston analysointi**
- **reaaliaikainen webkameran käyttö**

Tulokset näytetään käyttöliittymässä seuraavilla tavoilla:

- havaintolista
- videokuvan päälle piirretyt rajauslaatikot
- backendin palauttama raakamuotoinen JSON-vastaus

---

## 2. Järjestelmän osat

### Backend
Backend vastaa varsinaisesta analyysistä. Selain lähettää backendille joko:
- ladatun videotiedoston, tai
- yksittäisiä frameja webkamerasta

Backendin pitää olla käynnissä ennen kuin käyttöliittymä toimii oikein.

### Frontend
Selainkäyttöliittymässä käyttäjä voi:
- asettaa backendin osoitteen
- tarkistaa yhteyden
- ladata videon analysoitavaksi
- käynnistää webkameran
- tarkastella havaintoja ja JSON-vastausta

---

## 3. Mitä tarvitset ennen käyttöä

Ennen käyttöä varmista seuraavat asiat:

- Python-backend on asennettu ja käynnistettävissä
- projektin tiedostot ovat saatavilla
- selainkäyttöliittymä `docs/index.html` on avattavissa selaimessa
- tiedät backendin osoitteen, esimerkiksi `http://127.0.0.1:8000`
- käytössäsi on testivideo tai webkamera

Jos käytät webkameraa selaimessa, käyttö vaatii yleensä:
- `localhost`-ympäristön, tai
- HTTPS-yhteyden

---

## 4. Käyttöönotto yleiskuvana

Järjestelmän käyttö etenee yleensä näin:

1. Käynnistä Python-backend
2. Avaa selainkäyttöliittymä
3. Syötä backendin osoite
4. Tarkista yhteys
5. Valitse käyttötapa:
   - ladattu video
   - webkamera
6. Käynnistä analyysi
7. Tarkastele tuloksia käyttöliittymässä

---

## 5. Selainkäyttöliittymän käyttö

### 5.1 Backend-yhteyden määrittäminen

Käyttöliittymässä on kenttä **Backendin osoite**.

1. Kirjoita kenttään backendin URL, esimerkiksi:
   - `http://127.0.0.1:8000`
2. Paina **Tarkista yhteys**
3. Varmista, että yhteystestin tulos on onnistunut

Jos yhteys ei toimi:
- tarkista että backend on käynnissä
- tarkista että osoite on oikein
- tarkista että selain pääsee kyseiseen osoitteeseen

---

### 5.2 Ladatun videon analysointi

Tätä tilaa käytetään silloin, kun haluat analysoida valmiin videotiedoston.

1. Valitse videotiedosto kohdasta **Valitse videotiedosto**
2. Aseta tarvittaessa arvo kohtaan **Analysoi joka N:s frame**
3. Paina **Analysoi ladattu video**
4. Odota analyysin valmistumista
5. Tarkastele havaintolistaa ja videokuvan päälle piirrettyjä laatikoita

#### Mitä `Analysoi joka N:s frame` tarkoittaa

Tämä arvo vaikuttaa analyysin tiheyteen:

- pienempi arvo = useampi frame analysoidaan
- suurempi arvo = analyysi on kevyempi ja nopeampi, mutta havaintoja voi jäädä väliin

Esimerkki:
- `1` = analysoi jokainen frame
- `3` = analysoi joka kolmas frame

Hyvä käytännön lähtöarvo on pieni mutta ei liian raskas arvo, esimerkiksi `3`.

---

### 5.3 Webkameran käyttö

Tätä tilaa käytetään reaaliaikaiseen kokeiluun.

1. Aseta kohtaan **Näyteväli millisekunteina** haluttu arvo
2. Paina **Käynnistä webkamera**
3. Salli selaimelle kameran käyttö, jos selain kysyy lupaa
4. Tarkastele videokuvaa ja havaintoja reaaliaikaisesti
5. Lopeta painamalla **Pysäytä webkamera**

#### Mitä näyteväli tarkoittaa

Näyteväli määrää, kuinka usein selain lähettää frameja backendille.

- pienempi arvo = tiheämpi analyysi
- suurempi arvo = kevyempi kuormitus

Esimerkki:
- `250 ms` tarkoittaa, että kuvaa lähetetään noin neljä kertaa sekunnissa

Jos järjestelmä tuntuu raskaalta, kasvata näyteväliä.

---

## 6. Tulosten tulkinta

Käyttöliittymä näyttää analyysin tulokset useassa muodossa.

### Havaintolista
Havaintolista näyttää löydetyt kohdat videossa tai reaaliaikaisessa syötteessä.

Videotilassa listan riviä painamalla voidaan siirtyä vastaavaan kohtaan videossa.

### Rajauslaatikot
Käyttöliittymä piirtää havaintojen sijainnit videokuvan päälle.

Käyttäjä näkee visuaalisesti:
- missä havainto on
- kuinka suuri havainto on
- mihin kohtaan kuvaa havainto sijoittuu

### JSON-vastaus
Raaka JSON-vastaus näyttää backendin palauttamat tiedot tarkemmassa muodossa.

Tätä näkymää kannattaa käyttää erityisesti silloin, kun:
- haluat tarkistaa koordinaatit tarkasti
- haluat nähdä kaikki palautetut kentät
- haluat selvittää virhetilanteita

---

## 7. Tyypillinen käyttöprosessi

### Vaihtoehto A: analysoi video
1. Käynnistä backend
2. Avaa käyttöliittymä
3. Syötä backendin osoite
4. Tarkista yhteys
5. Lataa video
6. Aseta `frame_step`
7. Käynnistä analyysi
8. Tutki havaintolista ja laatikot

### Vaihtoehto B: käytä webkameraa
1. Käynnistä backend
2. Avaa käyttöliittymä
3. Syötä backendin osoite
4. Tarkista yhteys
5. Aseta näyteväli
6. Käynnistä webkamera
7. Salli kameran käyttö selaimessa
8. Tarkastele havaintoja reaaliajassa

---

## 8. Yleisimmät ongelmatilanteet

### Backend-yhteys ei toimi
Mahdollisia syitä:
- backend ei ole käynnissä
- backendin osoite on väärä
- portti on väärä
- selain ei pääse palvelimeen

Tarkista ensin yhteystesti.

### Video ei analysoidu
Mahdollisia syitä:
- videotiedosto ei ole kelvollinen
- backend ei tue tiedostoa odotetulla tavalla
- backend palauttaa virheen
- tiedosto on liian suuri tai hidas käsitellä

Tarkista JSON-vastaus ja backendin lokit.

### Webkamera ei käynnisty
Mahdollisia syitä:
- selain ei saanut kameran käyttöoikeutta
- käytössä ei ole HTTPS tai localhost
- toinen ohjelma käyttää kameraa
- selaimen asetukset estävät kameran käytön

### Tuloksia ei näy vaikka analyysi käynnistyy
Mahdollisia syitä:
- videossa ei ole tunnistettavaa kohdetta
- analysointiväli on liian harva
- näyteväli on liian suuri
- backendin tunnistuslogiikka tarvitsee säätöä

---






# capturing_frames-with_movement
For complete machine vision system is needed to have Raspberry Pi (most likely ver. 4) along with rest project files:

Project structure:
|--config
|  |-- gmg.json	
|  |-- mog.json
|-- output_gmg
|  |-- 20181014-143423.jpg
|  |-- ...
|-- output_mog
|  |-- 20200318-104253.jpg
|  |-- ...
|-- pyimadesearch  
|  |-- utils
|  |  |--_init_.py
|  |  |-- conf.py
|  |--__init_.py
|  |-- keyclipwriter.py

Machine vision application that captures motion picture frames in the video stream. The operation is based on buffering the frames so
that the frames are recorded before and after the movement. When motion is detected, any frames can be saved from the buffer to the disk.
Until no further motion is detected. Application use background subtraction and contour processing. 

Analyzing video (birds_10min.mp4):
(py3cv4) pi@raspberrypi:~/HobbyistBundle_Code/chapter09-bird_feeder_monitor $ python bird_mon.py --conf config/mog.json --video birds_10min.mp4

Analyzing cameras video stream:
(py3cv4) pi@raspberrypi:~/HobbyistBundle_Code/chapter09-bird_feeder_monitor $ python bird_mon.py --conf config/mog.json 
