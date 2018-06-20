#!/usr/bin/env bash
cd static/images/scraped_images
delay=$(awk -v min=50 -v max=300 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
convert -delay $delay -loop 0 *.jpg ../mix.gif
