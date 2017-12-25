#!/usr/bin/env bash
cd static/images/scraped_images
convert -delay 20 -loop 0 *.jpg mix.gif
