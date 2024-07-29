import os
import time
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
import math
from soco_cli import api

#pn532 = PN532_SPI(cs=4, reset=20, debug=False)
pn532 = PN532_UART(debug=False, reset=20)

#ic, ver, rev, support = pn532.get_firmware_version()
#print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()

def create_URI():
    """
    Reads an NTAG215 tag that was written using NFC Tools and returns
    a string URI containing a URI to music on Spotify, Apple Music,
    Tidal, or Deezer. URI is stored using the NDEF format.

    NDEF message structure
    Page 4: 03 XX D1 01
    03: Indicates start of NDEF message
    XX: represents payload length from this byte (non-standard)
    D1: Binary for 1101 0001 and is a NDEF Record Header flags byte
    01: Type Length (1 byte)

    Page 5: YY 55 ZZ AA
    YY: also payload length in bytes, including start & stop characters
    55: Type field ('U' for URI record)
    ZZ: URI Identifier (00 is no prefrix, 04 is https://)
    AA: Is the first byte of the payload (start character)
    FE is the stop character found on a later page
    """

    # Create list to hold page data
    URI = []

    # Read in page 5
    first_page = pn532.ntag2xx_read_block(5)

    # Store the length of the URI
    length_of_URI = first_page[0]

    # Store the type of URI
    URI_type = first_page[2]

    # Calculate which page will contain the stop character
    last_page = 6 + math.ceil( (length_of_URI-1)/4 )

    # Append the only URI character on page 5
    URI.append([first_page[3]])

    # Go through all pages that contain the URI until the stop
    # character, FE, is reached, then break from the loop
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
    URI_trimmed = URI_flat[:URI_flat.index(int('FE', 16))]

    # Convert the bytes into ASCII characters
    URI_ASCII = [chr(i) for i in URI_trimmed]

    # Create a string containing the characters
    URI_final = "".join(URI_ASCII)

    # If the URI type is 4, it is a https:// link
    if URI_type == 4:
        # sonos-cli requires https links to be in quotes
        URI_final = "'https://"+URI_final+"'"

    return URI_final

def play_URI(speaker, this_URI):
    # End any existing 3rd party sessions started from another app
    exit_code, output, error = api.run_command(speaker, "end_session")
    print(exit_code, output, error)

    # Clear the queue from any old albums / playlists
    exit_code, output, error = api.run_command(speaker, "clear_queue")
    print(exit_code, output, error)

    # Group all speakers together with {speaker} as the coordinator
    exit_code, output, error = api.run_command(speaker, "party")
    print(exit_code, output, error)

    # Load the URI
    exit_code, output, error = api.run_command(speaker, "sharelink", this_URI)
    print(exit_code, output, error)

    # Sets shuffle to off
    exit_code, output, error = api.run_command(speaker, "shuffle", "off")
    print(exit_code, output, error)

    # Play the URI
    exit_code, output, error = api.run_command(speaker, "play")
    print(exit_code, output, error)

    return f"Playing URI: {this_URI}"

def display_info(speaker):
    api.run_command(speaker, "album_art")
    api.run_command(speaker, "track")
    return None

# Initialize the UID to None for first time through
current_uid = None
coordinator = "Kitchen"

print('Waiting for RFID/NFC card to read from!')

while True:
    uid = None
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)

    # If a card was scanned, and its not the last card
    # that was read, then play the URI it contains
    if (uid is not None) and (uid != current_uid):
        current_uid = uid
        current_URI = create_URI()
        play_URI( coordinator, current_URI )
        GPIO.cleanup()

GPIO.cleanup()
