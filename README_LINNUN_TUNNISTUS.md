# Linnun tunnistusohjelman käyttöönotto

Tämä verkkosivu toimii käyttöliittymänä. Varsinainen linnun tunnistus tehdään Python-backendissä, joka pitää käynnistää omalla koneella. Pelkkä GitHub Pages -sivu ei yksin riitä, koska GitHub Pages ei aja Python-ohjelmia.

## Mitä tarvitset

Tarvitset:
- Python 3.12
- Git
- internetyhteyden ensimmäistä käynnistystä varten, jotta tarvittavat paketit ja mallipainot voidaan ladata
- webkameran tai videotiedoston

## 1. Lataa projekti koneellesi

Avaa terminaali ja suorita:

```bash
git clone https://github.com/kopja3/capturing_frames-with_movement.git
cd capturing_frames-with_movement
git checkout master
git pull origin master
```

## 2. Luo Python-ympäristö

### macOS ja Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --force-reinstall "numpy<2"
python -m pip install -r requirements-web.txt
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --force-reinstall "numpy<2"
python -m pip install -r requirements-web.txt
```

## 3. Käynnistä Python-backendi

Suorita tämä projektikansiossa:

```bash
uvicorn bird_backend_api_mask_stable:app --host 0.0.0.0 --port 8000
```

Kun kaikki toimii, terminaali näyttää rivin jossa näkyy, että palvelin kuuntelee portissa 8000.

## 4. Avaa verkkosivu

Avaa uusi terminaali samaan projektikansioon ja käynnistä staattinen web-palvelin:

```bash
python3 -m http.server 8081
```

Avaa sen jälkeen selaimessa:

```text
http://localhost:8081/docs/index_mask_stable.html
```

Jos portti 8081 on varattu, voit käyttää esimerkiksi porttia 8090:

```bash
python3 -m http.server 8090
```

ja avata selaimessa:

```text
http://localhost:8090/docs/index_mask_stable.html
```

## 5. Tarkista yhteys

Kun sivu aukeaa:
- jätä backend-osoitteeksi `http://127.0.0.1:8000`
- paina **Tarkista yhteys**

Jos yhteys toimii, voit käyttää ohjelmaa.

## 6. Käyttötavat

Sivulla on kaksi päätapaa.

### Videotiedosto
- valitse koneelta video
- paina **Analysoi ladattu video**

### Webkamera
- paina **Käynnistä webkamera**
- anna selaimelle lupa käyttää kameraa

## Mitä näet ruudulla

Ohjelma näyttää:
- liikkuviksi tulkitut pikselit läpinäkyvänä maskina videon päällä
- oranssit laatikot liikealueille
- vihreät laatikot linnuksi tunnistetuille kohteille
- koordinaatit pikseleinä muodossa `x1, y1, x2, y2`
- lisätietoa kuten maskin osuus, valon muutoksen määrä ja mahdollinen välkyntähylkäys

## Jos kuva välkkyy tai koko kuva menee maskiksi

Ohjelmassa on valmiiksi suodatus kameran automaattisten kirkkausmuutosten vähentämiseksi, mutta webkamerat voivat silti joskus säätää kuvaa voimakkaasti. Kokeile näitä:
- pidä valaistus tasaisena
- vältä vastavaloa
- pidä kamera paikallaan
- odota muutama sekunti käynnistyksen jälkeen, jotta taustamalli ehtii vakautua

## Yleisimmät ongelmat

### Sivu ei avaudu
- varmista että käynnistit `http.server`-komennon projektin juurikansiosta
- käytä oikeaa osoitetta, esimerkiksi `http://localhost:8081/docs/index_mask_stable.html`

### Backendiin ei saada yhteyttä
- varmista että `uvicorn` on käynnissä portissa 8000
- tarkista että sivulla backend-osoite on `http://127.0.0.1:8000`

### Portti on jo käytössä
- vaihda porttia, esimerkiksi 8081 tai 8090 web-sivulle
- backendille voit tarvittaessa käyttää myös toista porttia, mutta silloin sama portti pitää päivittää myös sivun backend-osoitteeseen

### `numpy` / `torch` / `_ARRAY_API` -virhe
- suorita ympäristössä tämä komento uudelleen:

```bash
python -m pip install --force-reinstall "numpy<2"
```

## Sulkeminen

Kun lopetat käytön:
- pysäytä backend `Ctrl-C`
- pysäytä web-palvelin `Ctrl-C`
