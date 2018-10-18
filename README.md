# matrix-display
### System Requirements
* node.js for build frontend (vuejs)
* PHP >= 7.1 for backend
* Redis for communicate python and php
* Python 3 for matrix-display daemon

### Install
#### Install node.js
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


### Build
```
cd ~/
git clone https://github.com/almajiro/matrix-display.git
cd matrix-display
cd frontend
yarn
```

### Development and Testing
```
cd ~/matrix-display/frontend
yarn dev
```