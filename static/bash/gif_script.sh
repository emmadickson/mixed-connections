#!/usr/bin/env bash
cd static/images/scraped_images
delay=$(jot -r 1  50 300)
convert -delay $delay -loop 0 *.jpg ../mix.gif
