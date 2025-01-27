# Sonos Jukebox
Inspired by [Tala](https://talaexe.com)'s [Spotify RFID Record Player](https://talaexe.com/moderndayrecordplayer)[[github](https://github.com/talaexe/Spotify-RFID-Record-Player)]

## Introduction

The hardware used in this project consists of:
* Rasberry Pi 3B with power supply and flash card
* [Waveshare PN532 NFC HAT](https://www.waveshare.com/wiki/PN532_NFC_HAT#Read_NTAG2XX_card)
* NTAG215 NFC tags

## NFC21X tag specifications
* page 11: (https://www.orangetags.com/wp-content/downloads/datasheet/NXP/NTAG213_215_216.pdf) 

## Hardware configuration
Connecting the hardware and setting the jumpers/pins

## Software configuration

### Installing Raspberry Pi OS

### Creating a `venv` environment
```bash
python -m venv <path_to_sonosjukebox>/venv/
```

```bash
source <path_to_sonosjukebox>/venv/bin/activate
```

### Installing required Python libraries
```bash
pip install -r requirements.txt
```

Libraries included in `requirements.txt`:
* [`RPi.GPIO`](https://pypi.org/project/RPi.GPIO/)
* [`spidev`](https://pypi.org/project/spidev/)
* [`soco-cli`](https://github.com/avantrec/soco-cli)
* [`serial`](https://pypi.org/project/serial/)

### Downloading `sonosjukebox` files

### Configuring `crontab`

## Understanding the `player.py` script


## Future Ideas
Add e-ink display like (https://www.adafruit.com/product/3743). Might need to change NFC hardware to not have the display cover up the NFC reader location?
