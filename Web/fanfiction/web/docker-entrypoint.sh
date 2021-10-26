#!/usr/bin/env bash
set -e

# Run redis
sudo -u redis /usr/bin/redis-server --daemonize yes

# Run bot
/usr/bin/supervisord -c /etc/supervisord.conf

# Run cron for clearing up box
cron

# Run apache
exec "$@"