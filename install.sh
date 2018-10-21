#!/bin/bash

echo ""
echo "                  _        _                _ _           _              "
echo "                 | |      (_)              | (_)         | |             "
echo "  _ __ ___   __ _| |_ _ __ ___  ________ __| |_ ___ _ __ | | __ _ _   _  "
echo " | '_ \` _ \ / _\` | __| '__| \ \/ /______/ _\` | / __| '_ \| |/ _\` | | | | "
echo " | | | | | | (_| | |_| |  | |>  <      | (_| | \__ \ |_) | | (_| | |_| | "
echo " |_| |_| |_|\__,_|\__|_|  |_/_/\_\      \__,_|_|___/ .__/|_|\__,_|\__, | "
echo "                                                   | |             __/ | "
echo "                                                   |_|            |___/  "
echo ""
echo "matrix-display command line installer script"

DESTINATION="/home/pi"

sudo apt-get update
sudo apt-get install -y curl

echo "--- Install node.js ---"
echo "Install nodebrew"
curl -L git.io/nodebrew | perl - setup
echo "export PATH=$HOME/.nodebrew/current/bin:$PATH" >> ${DESTINATION}/.bashrc
source ${DESTINATION}/.bashrc
nodebrew install stable
nodebrew use stable

echo "Install yarn"
npm install -g yarn

echo "--- Install PHP ---"
echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" >> /etc/apt/sources.list
apt-get update
apt-get install -y php7.2 php7.2-fpm php7.2-mbstring php7.2-xml

echo "--- Install yarn ---"
apt-get remove --purge -y apache2
apt-get install -y nginx