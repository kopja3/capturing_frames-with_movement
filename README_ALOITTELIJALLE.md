# Aloittelijan ohje

Tämä ohje näyttää vaihe vaiheelta, miten ohjelma asennetaan omalle koneelle ja miten selainkäyttöliittymä käynnistetään komentoriviltä.

## Mitä tarvitset

Tarvitset nämä ennen aloittamista:

- Python 3.12
- Git
- internetyhteyden ensimmäistä käynnistystä varten
- webkameran tai videotiedoston

## 1. Lataa projekti koneelle

Avaa terminaali tai komentorivi ja suorita:

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

Pidä tämä terminaali auki ja suorita projektikansiossa:

```bash
uvicorn bird_backend_api_mask_stable:app --host 0.0.0.0 --port 8000
```

Kun kaikki toimii, palvelin kuuntelee portissa 8000.

## 4. Käynnistä paikallinen web-palvelin

Avaa toinen terminaali samaan projektikansioon ja suorita:

### macOS ja Linux

```bash
python3 -m http.server 8081
```

### Windows PowerShell

```powershell
py -3 -m http.server 8081
```

Sivun osoite on:

```text
http://localhost:8081/docs/index_mask_stable_camera_select.html
```

## 5. Avaa selain komentoriviltä

### Windows PowerShell

```powershell
start http://localhost:8081/docs/index_mask_stable_camera_select.html
```

### macOS

```bash
open http://localhost:8081/docs/index_mask_stable_camera_select.html
```

### Linux

```bash
xdg-open http://localhost:8081/docs/index_mask_stable_camera_select.html
```

## 6. Tarkista yhteys sivulla

Kun sivu aukeaa:

- jätä backend-osoitteeksi `http://127.0.0.1:8000`
- paina **Tarkista yhteys**

Jos yhteys toimii, voit käyttää ohjelmaa.

## 7. Käyttö

### Videotiedosto

- valitse koneelta video
- paina **Analysoi ladattu video**

### USB-kamera tai webkamera

- paina **Päivitä kameraluettelo**
- valitse kamera listasta
- paina **Käynnistä valittu kamera**
- anna selaimelle lupa käyttää kameraa

## Yleisimmät ongelmat

### Selain antaa 404 virheen

Et ole projektin oikeassa kansiossa tai paikallinen kopio ei ole ajan tasalla.

Suorita:

```bash
git pull origin master
ls docs
```

### Backendiin ei saada yhteyttä

- varmista että `uvicorn` on käynnissä portissa 8000
- tarkista että sivulla backend-osoite on `http://127.0.0.1:8000`

### Kamera ei käynnisty

- varmista että avasit sivun osoitteesta `localhost`
- varmista että annoit selaimelle kameran käyttöluvan

### Portti on jo käytössä

Voit vaihtaa web-sivun portin esimerkiksi näin:

```bash
python3 -m http.server 8090
```

Silloin osoite on:

```text
http://localhost:8090/docs/index_mask_stable_camera_select.html
```

## Sulkeminen

Kun lopetat käytön:

- pysäytä backend `Ctrl-C`
- pysäytä web-palvelin `Ctrl-C`
