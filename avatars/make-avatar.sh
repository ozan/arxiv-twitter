#!/usr/bin/env bash

# use imagemagick to create avatar from name, eg:
# ./make-avatar 'CS\nCV'

set -euo pipefail
IFS=$'\n\t'

[ $# -eq 0 ] && echo "Error: must supply name" && exit 1

CAPTION=$1
NAME=${CAPTION/'\n'/}

convert \
  -background '#00ff00' \
  -fill '#005500' \
  -border 20 \
  -font 'Helvetica-Bold' \
  -size 512x512 \
  -pointsize 240 \
  -gravity south \
  caption:"${CAPTION}" \
  "${NAME}.png"

echo "Created ${NAME}.png"
