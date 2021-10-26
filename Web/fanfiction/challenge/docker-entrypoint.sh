#!/usr/bin/env bash
set -e

# Run redis
sudo -u redis /usr/bin/redis-server --daemonize yes

# Run bot
/usr/bin/supervisord -c /etc/supervisord.conf

# Run apache
exec "$@"