# Selain + Python-backend linnun tunnistukseen

Tässä toteutuksessa selain toimii käyttöliittymänä ja Python tekee varsinaisen analyysin.

## Uudet tiedostot

- `docs/index.html` = selainkäyttöliittymä videolle ja webkameralle
- `bird_backend_api.py` = FastAPI-backend linnun tunnistukseen
- `requirements-web.txt` = backendin riippuvuudet

## Asennus

1. Luo virtuaaliympäristö ja asenna paketit:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-web.txt
```

2. Käynnistä backend:

```bash
uvicorn bird_backend_api:app --host 0.0.0.0 --port 8000
```

3. Avaa selainkäyttöliittymä:

- GitHub Pagesista polusta `/docs/`, tai
- paikallisesti esimerkiksi komennolla:

```bash
python -m http.server 8080
```

ja avaa selaimessa `http://localhost:8080/docs/`.

## Mitä tämä tekee

- lataa videotiedoston backendille analysoitavaksi
- voi lähettää webkamerasta yksittäisiä frameja backendille
- piirtää havaitun linnun rajauslaatikon videon päälle
- näyttää koordinaatit pikseleinä muodossa:
  - `x1, y1` = vasen yläkulma
  - `x2, y2` = oikea alakulma
  - `cx, cy` = keskipiste

## Oletusmalli

Backend yrittää ladata oletuksena painotiedoston:

```text
yolo11n.pt
```

Voit vaihtaa sen ympäristömuuttujalla:

```bash
export BIRD_MODEL_WEIGHTS=/polku/oma_malli.pt
```

Jos käytät yleismallia, backend suodattaa ulos vain `bird`-luokan havainnot.

## Motion gate

Backend käyttää liikkeentunnistusta porttina ennen lintumallia. Tämä vähentää turhia malliajoja. Sen voi kytkeä pois:

```bash
export ENABLE_MOTION_GATE=0
```

## Hyödyllisiä asetuksia

```bash
export MODEL_CONFIDENCE=0.25
export VIDEO_FRAME_STEP=3
export MOTION_MIN_AREA=900
export MOTION_RESIZE_WIDTH=640
```

## Huomioita

- GitHub Pages ei aja Pythonia, joten backend pitää ajaa erikseen.
- Jos käyttöliittymä ajetaan HTTPS:n yli, backendin kannattaa olla myös HTTPS:n takana.
- Webkameran käyttö toimii selaimessa vain suojatussa kontekstissa.
- Paras tarkkuus tulee omalla bird-only -mallilla. Yleismalli on hyvä lähtökohta, mutta ei paras mahdollinen lintulaji- tai pienkohdetarkkuus.
