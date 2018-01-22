#!/usr/bin/env bash
cd static/images/scraped_images
convert -delay 50 -loop 0 *.jpg mix.gif
