import os
import time

URI = ""
scanned = False

if not scanned:
  # look to see if URI gets updated

if scanned:
  URI = "spotify:album:1ZwkNGxlonmG4bjmLbV1Rr"
  os.system("sonos bedroom clear_queue")
  os.system("sonos bedroom party")
  os.system(f"sonos bedroom sharelink '{URI}'")
  os.system("sonos bedroom play")
  scanned = False
  time.sleep(3)
