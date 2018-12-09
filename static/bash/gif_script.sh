#!/usr/bin/env bash

# This script creates the gif that should serve as the sites icon.
# This works with scrape_job on the backend computer to generate a new site icon.

cd static/images/scraped_images
delay=$(awk -v min=50 -v max=300 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
convert -delay $delay -loop 0 *.jpg ../mix.gif
