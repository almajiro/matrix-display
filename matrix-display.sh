#!/bin/bash

start_display() {
  sudo service nginx start
  sudo service php7.2-fpm start
  sudo systemctl start matrix-display.service
}

stop_display() {
  sudo service nginx stop
  sudo service php7.2-fpm stop
  sudo systemctl stop matrix-display.service
}

restart_display() {
  sudo service nginx restart
  sudo service php7.2-fpm restart
  sudo systemctl restart matrix-display.service
}

case "$1" in
  start) start_display ;;
  stop) stop_dispaly ;;
  restart) restart_display ;;
  *) echo "usage: $0 start|stop|restart" >&2
    exit 1;
    ;;
esac
