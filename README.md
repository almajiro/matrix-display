# matrix-display
### System Requirements
* node.js for build frontend (vuejs)
* PHP >= 7.1 for backend
* Redis for communicate python and php
* Python 3 for matrix-display daemon

### Install
#### node.js
use nodebrew
```
curl -L git.io/nodebrew | perl - setup
vim or nano ~/.bashrc
add "export PATH=$HOME/.nodebrew/current/bin:$PATH"
source ~/.bashrc
nodebrew install stable
nodebrew use stable
```
And install yarn for build frontend
```
npm install -g yarn
```
#### PHP
```
echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" >> /etc/apt/sources.list
apt-get update
apt-get install -y php7.2 php7.2-fpm php7.2-mbstring php7.2-xml
```
#### nginx
If you already installed apache, you need to uninstall them.
```
apt-get remove --purge -y apache2
```
Install nginx
```
apt-get install -y nginx
```

### Build
#### vue.js (nuxt.js)
```
cd ~/
git clone https://github.com/almajiro/matrix-display.git
cd matrix-display/frontend
yarn
```
#### Lumen
```
cd ~/
cd matrix-display/backend
composer install --no-dev
cp .env.example .env
```

### Development and Testing
```
cd ~/matrix-display/frontend
yarn dev
```