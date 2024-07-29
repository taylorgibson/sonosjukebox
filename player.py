import os
import time
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
import math

#pn532 = PN532_SPI(cs=4, reset=20, debug=False)
pn532 = PN532_UART(debug=False, reset=20)

#ic, ver, rev, support = pn532.get_firmware_version()
#print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()



def create_URI():
    # Create list to hold page data
    URI = []
# NDEF message structure
# Page 4: 03 XX D1 01
# 03: Indicates start of NDEF message
# XX: represents payload length from this byte (non-standard)
# D1: Binary for 1101 0001 and is a NDEF Record Header flags byte
# 01: Type Length (1 byte)
#
# Page 5: YY 55 ZZ AA
# YY: also payload length in bytes, including start & stop characters
# 55: Type field ('U' for URI record)
# ZZ: URI Identifier (00 is no prefrix, 04 is https://)
# AA: Is the first byte of the payload (start character)
#
# FE is the stop character found on a later page

    first_page = pn532.ntag2xx_read_block(5)
    length_of_URI = first_page[0]
    URI_type = first_page[2]
    last_page = 6 + math.ceil( (length_of_URI-1)/4 )

    # Append the only URI character on page 5 since we have it already
    URI.append([first_page[3]])

    for i in range(6, last_page ):
        page = pn532.ntag2xx_read_block(i)
        try:
            URI.append([x for x in page])
        except nfc.PN532Error as e:
            print(e.errmsg)
            break
        if b'\xfe' in page:
            break

    # Create a flat list of all the bytes that contain the URI
    URI_flat = [item for row in URI for item in row]

    # Only keep the bytes up to but not including the stop character
    URI_trimmed = URI_flat[:URI_flat.index(254)]

    # Convert the bytes into ASCII characters
    URI_ASCII = [chr(i) for i in URI_trimmed]

    # Create a string containing the characters
    URI_final = "".join(URI_ASCII)

    # If the URI type is 4, it is a https:// link
    if URI_type == 4:
        URI_final = 'https://'+URI_final

    return URI_final

def play_URI(URI):
    os.system("sonos bedroom clear_queue")
    os.system("sonos bedroom party")
    os.system(f"sonos bedroom sharelink '{URI}'")
    os.system("sonos bedroom play")
    print('Playing URI: ', uri)

return None

# Initialize the UID to None for first time through
current_uid = None

print('Waiting for RFID/NFC card to read from!')

while True:

    while True:
        uid = None
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            if uid != current_uid:
                current_uid = uid
                # os.system('clear')
                # print('Waiting for RFID/NFC card to read from!')
                play_URI( create_URI() )
                GPIO.cleanup()
            break
#    print('Found card with UID:', [hex(i) for i in uid])

GPIO.cleanup()

#if not scanned:
#if scanned:
#  URI = "spotify:album:1ZwkNGxlonmG4bjmLbV1Rr"
#  )
#  os.system("sonos bedroom track") # Shows info on current track
#  os.system("sonos bedroom album_art") # returns URL of current album art
#  scanned = False
#  time.sleep(3)
