#!/bin/bash
set -x

export TMPDIR=/app
#remove existng from restart
chattr -i /app/flag_*.txt
rm /app/flag_*.txt
#new flag name
FILENAME=$(mktemp --suffix=.txt flag_XXXXXX)
#add flag
echo 'WMG{n0w_y0Ur3_p0Pp1n_sH3llz}' > $FILENAME && chown root:root $FILENAME && chmod 555 $FILENAME && chattr +i $FILENAME
#remove prestart script
rm /app/prestart.sh
#execute original entrypoint as www-data
exec gosu www-data /start.sh "$@"