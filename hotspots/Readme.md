# Hotspots

## Editor

### hotspot-editor.py

args:
--filename
--radius

This script will fire up the webcam.

Right click - freeze the image from the web cam.

Left click - once image is frozen, anywhere you click will create a hotspot circle and the x,y,radius will be capture.

Clicking inside the circle again, deletes the hotspot

'q' - to quit the script.

Upon quit, the normalized x,y, radius of all hotspots will be written to a file with name, hotspots.csv by default.

## Test

### hotspot-reader-test.py

This script will fire up the webcam and read the hotspots.csv ( or param for filename ) and draw the hotspots in the video window

